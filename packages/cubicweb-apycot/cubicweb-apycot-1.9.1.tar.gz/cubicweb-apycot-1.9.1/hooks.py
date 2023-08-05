"""this module contains server side hooks for notification about test status
changes

:organization: Logilab
:copyright: 2009-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
:license: General Public License version 2 - http://www.gnu.org/licenses
"""
__docformat__ = "restructuredtext en"

from datetime import datetime, timedelta

from cubicweb.selectors import implements
from cubicweb.uilib import text_cut
from cubicweb.server import hook
from cubicweb.hooks import notification as notifhooks
from cubicweb.sobjects import notification as notifviews

from cubes.vcsfile.entities import _MARKER
from cubes.apycot.entities import bot_proxy, vcsrepo_apycot_info

# automatic test launching #####################################################

def start_test(session, period):
    tostart = set()
    rql = ('Any TC, PE, PEN, TCN, TCS '
           'WHERE TC use_environment PE, PE name PEN, '
           'TC start_mode %(sm)s, TC in_state S, S name "activated", '
           'TC name TCN, TC start_rev_deps TCS')
    for tc in session.execute(rql, {'sm': period}).entities():
        env = tc.environment
        if not env.repository:
            tostart.add((env.name, tc.name, tc.start_rev_deps, None))
        else:
            # XXX check every active branch if no branch specified
            branch = tc.apycot_configuration.get('branch', _MARKER)
            head = env.repository.branch_head(branch)
            if head is None:
                # No head found (in the case of branch specific test config)
                continue
            # only start test if this config hasn't been
            # executed against current branch head
            if session.execute(
                'Any TE WHERE TE using_revision REV, REV eid %(rev)s, '
                'TE using_config TC, TC eid %(tc)s',
                {'rev': head.eid, 'tc': tc.eid}):
                # This rev have already been tested
                continue
            tostart.add((env.name, tc.name, tc.start_rev_deps, head.branch))
    return tostart


class ServerStartupHook(hook.Hook):
    """add looping task to automatically start tests
    """
    __regid__ = 'apycot.startup'
    events = ('server_startup',)
    def __call__(self):
        if not self.repo.config['test-master']:
            return
        # XXX use named args and inner functions to avoid referencing globals
        # which may cause reloading pb
        def check_test_to_start(repo, datetime=datetime, start_test=start_test,
                                StartTestsOp=StartTestsOp):
            now = datetime.now()
            tostart = set()
            session = repo.internal_session()
            try:
                # XXX only start task for environment which have changed in the
                # given interval
                tostart |= start_test(session, 'hourly')
                if now.hour == 1:
                    tostart |= start_test(session, 'daily')
                if now.isoweekday() == 1:
                    tostart |= start_test(session, 'weekly')
                if now.day == 1:
                    tostart |= start_test(session, 'monthly')
                if tostart:
                    StartTestsOp(session, tostart)
                session.commit()
            finally:
                session.close()
        self.repo.looping_task(60*60, check_test_to_start, self.repo)
        cleanupdelay = self.repo.config['test-exec-cleanup-delay']
        if not cleanupdelay:
            return # no auto cleanup
        cleanupinterval = min(60*60*24, cleanupdelay)
        def cleanup_test_execs(repo, delay=timedelta(seconds=cleanupdelay),
                               now=datetime.now):
            session = repo.internal_session()
            mindate = now() - delay
            try:
                session.execute('DELETE TestExecution TE '
                                'WHERE TE modification_date < %(min)s',
                                {'min': mindate})
                session.commit()
            finally:
                session.close()
        self.repo.looping_task(cleanupinterval, cleanup_test_execs, self.repo)


class StartTestAfterAddVersionContent(hook.Hook):
    __regid__ = 'apycot.start_test_on_new_rev'
    __select__ = hook.Hook.__select__ & implements('Revision')
    events = ('after_add_entity',)

    def __call__(self):
        vcsrepo = self.entity.repository
        for pe in vcsrepo.reverse_local_repository:
            if not pe.vcs_path:
                StartTestsOp(self._cw, set(
                    (pe.name, tc.name, tc.start_rev_deps, self.entity.branch)
                    for tc in pe.reverse_use_environment
                    if tc.start_mode == 'on new revision'
                    and tc.match_branch(self.entity.branch)))
            else:
                StartTestsIfMatchOp(self._cw, revision=self.entity, pe=pe)
        # when a test is started, it may use some revision of dependency's
        # repositories that may not be already imported by vcsfile. So when it
        # try to create a link between the execution and the revision, it
        # fails. In such case the information is kept as a CheckResultInfo
        # object, use it to create the link later when the changeset is
        # imported.
        for cri in self._cw.execute(
            'Any CRI, X WHERE CRI for_check X, CRI type "revision", '
            'CRI label ~= %(repo)s, CRI value %(cs)s',
            {'cs': self.entity.changeset,
             # safety belt in case of duplicated short changeset. XXX useful?
             'repo': '%s:%s%%' % vcsrepo_apycot_info(vcsrepo)}).entities():
            cri.parent.set_relations(using_revision=self.entity)
            cri.delete()


class StartTestsIfMatchOp(hook.Operation):

    def precommit_event(self):
        rql = ('Any TC, PE, PEN, TCN, TCS WHERE TC use_environment PE, REV eid %(rev)s,'
               'PE name PEN, PE eid %(pe)s, PE vcs_path PEP, TC name TCN, '
               'TC start_rev_deps TCS, '
               'TC start_mode %(sm)s, TC in_state S, S name "activated", '
               'VC from_revision REV, '
               'VC content_for VF, VF directory ~= PEP + "%"'
               )
        rset = self.session.execute(rql, {'sm': 'on new revision',
                                          'rev': self.revision.eid,
                                          'pe': self.pe.eid})
        if rset:
            branch = self.revision.branch
            testconfigs = set((row[2], row[3], row[4], self.revision.branch)
                               for i, row in enumerate(rset)
                               if rset.get_entity(i, 0).match_branch(branch))
            StartTestsOp(self.session, testconfigs)


class StartTestsOp(hook.SingleLastOperation):
    def __init__(self, session, tests):
        self.tests = tests
        super(StartTestsOp, self).__init__(session)

    def register(self, session):
        previous = super(StartTestsOp, self).register(session)
        if previous:
            self.tests |= previous.tests

    def commit_event(self):
        self.session.repo.threaded_task(self.start_tests)

    def start_tests(self):
        session = self.session
        config = session.vreg.config
        try:
            bot = bot_proxy(config, session.transaction_data)
        except Exception, ex:
            self.error('cant contact apycot bot: %s', ex)
            # XXX create a TestExecution to report the attempt to launch test
            return
        # XXX make start_rev_deps=True configurable
        full_pyro_id = ':%(pyro-ns-group)s.%(pyro-instance-id)s' % config
        for envname, tcname, startrevdeps, branch in self.tests:
            try:
                bot.queue_task(envname, tcname,
                               branch=branch, start_rev_deps=startrevdeps,
                               cwinstid=full_pyro_id)
            except Exception, ex:
                self.error('cant start test %s: %s', tcname, ex)
                # XXX create a TestExecution to report the attempt to launch test
                return


# notifications ################################################################

class ExecStatusChangeView(notifviews.NotificationView):
    __regid__ = 'exstchange'
    __select__ = implements('TestExecution')

    content = '''The following changes occured between executions on branch %(branch)s:

%(changelist)s

Imported changes occured between %(ex1time)s and %(ex2time)s:
%(vcschanges)s

URL: %(url)s
'''

    def subject(self):
        entity = self.cw_rset.get_entity(0, 0)
        changes = entity.status_changes()
        testconfig = entity.configuration.dc_title()
        if entity.branch:
            testconfig = u'%s#%s' % (testconfig, entity.branch)
        if len(changes) == 1:
            name, (fromstate, tostate) = changes.items()[0]
            fromstate, tostate = fromstate.status, tostate.status
            subject = '%s: %s -> %s (%s)' % (
                testconfig, self._cw._(fromstate), self._cw._(tostate), name)
        else:
            count = {}
            for fromstate, tostate in entity.status_changes().values():
                fromstate, tostate = fromstate.status, tostate.status
                try:
                    count[tostate] += 1
                except KeyError:
                    count[tostate] = 1
            resume = ', '.join('%s %s' % (num, self._cw._(state))
                               for state, num in count.items())
            subject = self._cw._('%s now has %s') % (testconfig, resume)
        return '[%s] %s' % (self._cw.vreg.config.appid, subject)

    def context(self):
        entity = self.cw_rset.get_entity(0, 0)
        prevexec = entity.previous_entity()
        ctx  = super(ExecStatusChangeView, self).context()
        ctx['ex1time'] = prevexec.printable_value('starttime')
        ctx['ex2time'] = entity.printable_value('starttime')
        ctx['branch'] = entity.branch
        chgs = []
        _ = self._cw._
        for name, (fromstate, tostate) in sorted(entity.status_changes().items()):
            name = _(name)
            fromstate, tostate = _(fromstate.status), _(tostate.status)
            chg = _('%(name)s status changed from %(fromstate)s to %(tostate)s')
            chgs.append('* ' + (chg % locals()))
        ctx['changelist'] = '\n'.join(chgs)
        vcschanges = []
        for env in [entity.configuration.environment] + entity.configuration.dependencies():
            if env.repository:
                vcsrepo = env.repository
                vcsrepochanges = []
                lrev1 = prevexec.repository_revision(env.repository)
                lrev2 = entity.repository_revision(env.repository)
                if lrev1 and lrev2:
                    for rev in self._cw.execute(
                        'Any REV, REVA, REVD, REVR, REVC ORDERBY REV '
                        'WHERE REV from_repository R, R eid %(r)s, REV branch %(branch)s, '
                        'REV revision > %(lrev1)s, REV revision <= %(lrev2)s, '
                        'REV author REVA, REV description REVD, '
                        'REV revision REVR, REV changeset REVC',
                        {'r': env.repository.eid,
                         'branch': lrev2.branch or env.repository.default_branch(),
                         'lrev1': lrev1.revision, 'lrev2': lrev2.revision}).entities():
                        msg = text_cut(rev.description)
                        vcsrepochanges.append('  - %s by %s:%s' % (
                            rev.dc_title(), rev.author, msg))
                    if vcsrepochanges:
                        vcschanges.append('* in repository %s: \n%s' % (
                            env.repository.path, '\n'.join(vcsrepochanges)))
        if vcschanges:
            ctx['vcschanges'] = '\n'.join(vcschanges)
        else:
            ctx['vcschanges'] = self._cw._('* no change found in known repositories')
        return ctx


class ExecStatusChangeHook(hook.Hook):
    __regid__ = 'apycot.send_reports_on_exec_status_change'
    __select__ = hook.Hook.__select__ & implements('TestExecution')
    events = ('after_update_entity',)

    def __call__(self):
        # end of test execution : set endtime
        entity = self.entity
        if 'endtime' in entity.edited_attributes and entity.status_changes():
            view = self._cw.vreg['views'].select(
                'exstchange', self._cw, rset=entity.cw_rset, row=entity.cw_row,
                col=entity.cw_col)
            notifhooks.RenderAndSendNotificationView(self._cw, view=view)


try:
    from cubes.nosylist import hooks as nosylist
except ImportError:
    pass
else:
    # XXX that does not mean the nosylist cube is used by the instance, but it
    # shouldn't matter anyway
    nosylist.S_RELS |= set(('has_apycot_environment',))
    nosylist.O_RELS |= set(('use_environment', 'using_config'))
