"""this module contains the primary views for apycot entities

:organization: Logilab
:copyright: 2008-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
:license: General Public License version 2 - http://www.gnu.org/licenses
"""
__docformat__ = "restructuredtext en"

from logilab.mtconverter import xml_escape

from cubicweb import Unauthorized, NoSelectableObject, tags
from cubicweb.selectors import (implements, has_related_entities, none_rset,
                                match_user_groups, match_kwargs, score_entity)
from cubicweb.view import EntityView
from cubicweb.web import (Redirect, uicfg, component, box,
                          formfields as ff, formwidgets as fwdgs)
from cubicweb.web.views import primary, tabs, forms, baseviews, tableview
from cubicweb.web.views import ibreadcrumbs, idownloadable

from cubes.apycot.entities import bot_proxy
from cubes.apycot.views import anchor_name
from cubes.apycot.logformat import log_to_html


_pvs = uicfg.primaryview_section
_pvdc = uicfg.primaryview_display_ctrl


class InfoLogMixin(object):

    def display_info_section(self, entity):
        rset = self._cw.execute(
            'Any X,T,L,V ORDERBY T,L WHERE X is CheckResultInfo, '
            'X type T, X label L, X value V, X for_check AE, AE eid %(ae)s',
            {'ae': entity.eid})
        title = self._cw._('execution information')
        self.wview('table', rset, 'null', title=title, displaycols=range(1, 4),
                   divid='info%s'%entity.eid)

    def display_log_section(self, entity):
        if entity.log:
            self.w(u'<h3>%s</h3>' % self._cw._('logs'))
            log_to_html(self._cw, entity.log, self.w)


# ProjectEnvironment ###########################################################

_pvs.tag_subject_of(('ProjectEnvironment', 'local_repository', '*'), 'relations')
_pvs.tag_object_of(('*', 'use_environment', 'ProjectEnvironment'), 'relations')
_pvs.tag_object_of(('*', 'needs_checkout', 'ProjectEnvironment'), 'sideboxes')
_pvdc.tag_object_of(('*', 'use_environment', 'ProjectEnvironment'),
                    {'vid': 'apycot.pe.tc'})
_pvdc.tag_attribute(('ProjectEnvironment', 'vcs_repository'), {'vid': 'urlattr'})

_pvs.tag_attribute(('ProjectEnvironment', 'name'), 'hidden')
_pvs.tag_attribute(('ProjectEnvironment', 'check_preprocessors'), 'hidden')
# in breadcrumb
_pvs.tag_object_of(('*', 'has_apycot_environment', 'ProjectEnvironment'), 'hidden')

class ProjectEnvironmentPrimaryView(tabs.TabbedPrimaryView):
    __select__ = implements('ProjectEnvironment')

    tabs = [_('pe_config'), _('pe_executions')]
    default_tab = 'pe_config'


class PEConfigTab(tabs.PrimaryTab):
    __regid__ = 'pe_config'
    __select__ = implements('ProjectEnvironment')

    def render_entity_attributes(self, entity):
        super(PEConfigTab, self).render_entity_attributes(entity)
        self.w(u'<h4>%s</h4>' % self._cw._('check_preprocessors'))
        valdict = entity.apycot_preprocessors
        if not valdict:
            msg = self._cw._('this environment has no preprocessor configured.')
            self.w('<p>%s</p>' % msg)
        else:
            headers = (self._cw._('install type'), self._cw._('preprocessor'))
            self.wview('pyvaltable', headers=headers,
                       pyvalue=sorted(valdict.items()))



class PEExecutionTab(EntityView):
    __regid__ = 'pe_executions'
    __select__ = (implements('ProjectEnvironment') &
                  has_related_entities('use_environment', 'object'))

    def cell_call(self, row, col):
        rset = self._cw.execute(
            'Any TC,T,T,TB,TST,TET,TF, TS ORDERBY TST DESC WHERE '
            'T status TS, T using_config TC, T branch TB, '
            'T starttime TST, T endtime TET, T log_file TF?, '
            'TC use_environment PE, PE eid %(pe)s',
            {'pe': self.cw_rset[row][col]})
        self.wview('apycot.te.summarytable', rset, 'noresult')


class PETestConfigView(EntityView):
    __regid__ = 'apycot.pe.tc'
    __select__ = implements('TestConfig')
    def call(self):
        self.w(u'<table>')
        for tc in self.cw_rset.entities():
            self.w(u'<tr><td>')
            tc.view('oneline', w=self.w)
            self.w(u'</td><td>')
            try:
                form = self._cw.vreg['forms'].select('starttestform', self._cw,
                                                     entity=tc)
            except NoSelectableObject:
                self.w(u'&#160;')
            else:
                self.w(form.render())
            self.w(u'</td></tr>')
        self.w(u'</table>')


# TestConfig, TestConfigGroup ##################################################

_pvs.tag_subject_of(('*', 'use_group', '*'), 'attributes')
_pvs.tag_subject_of(('*', 'needs_checkout', '*'), 'sideboxes')
_pvdc.tag_object_of(('*', 'use_group', '*'), {'subvid': 'outofcontext'})
_pvs.tag_object_of(('TestExecution', 'using_config', 'TestConfig'), 'hidden')
_pvs.tag_attribute(('TestConfigGroup', 'name'), 'hidden')
_pvs.tag_attribute(('TestConfig', 'name'), 'hidden')
_pvs.tag_attribute(('*', 'check_environment'), 'hidden')
_pvs.tag_attribute(('*', 'check_config'), 'hidden')
_pvdc.tag_attribute(('*', 'checks'), {'vid': 'tc.checks'})

class TCCheckView(EntityView):
    __regid__ = 'tc.checks'
    __select__ = (implements('TestConfig', 'TestConfigGroup')
                  & match_kwargs('rtype', 'role'))

    def cell_call(self, row, col, rtype, role):
        assert rtype == 'checks' and role == 'subject'
        entity = self.cw_rset.get_entity(row, col)
        try:
            owner, checks = entity.all_checks_and_owner()
        except TypeError: # no checks found
            value = self._cw._('no value specified')
        else:
            value = xml_escape(u', '.join(checks))
            if owner.eid != entity.eid:
                value += self._cw._(u' <i>(from group %s)</i>') % owner.view('oneline')
        self.w(value)

class TCDescriptionMixIn(object):

    def render_entity_attributes(self, entity):
        super(TCDescriptionMixIn, self).render_entity_attributes(entity)
        groups = entity.config_parts()
        for dictattr, label in (('apycot_configuration', self._cw._('check_config')),
                                ('apycot_process_environment', self._cw._('check_environment'))):
            valdict = getattr(entity, dictattr)
            owndict = getattr(entity, 'my_%s' % dictattr)
            values = []
            for key, val in valdict.items():
                if key in owndict:
                    group = ''
                else:
                    for group in groups:
                        gvaldict = getattr(group, 'my_%s' % dictattr)
                        if key in gvaldict:
                            group = group.view('oneline')
                            break
                    else:
                        group = u'???'
                values.append( (xml_escape(key), xml_escape(val), group) )
            if valdict:
                self.w(u'<h4>%s</h4>' % label)
                headers = (self._cw._('key'), self._cw._('value'),
                           self._cw._('inherited from group'))
                self.wview('pyvaltable', pyvalue=sorted(values), headers=headers)
            else:
                self.field(label, self._cw._('no value specified'), tr=False)


class TestConfigGroupPrimaryView(TCDescriptionMixIn, primary.PrimaryView):
    __select__ = implements('TestConfigGroup')


class TestConfigPrimaryView(tabs.TabbedPrimaryView):
    __select__ = implements('TestConfig')

    tabs = [_('tc_config'), _('tc_execution')]
    default_tab = 'tc_config'


class TCConfigTab(TCDescriptionMixIn, tabs.PrimaryTab):
    __select__ = implements('TestConfig')
    __regid__ = 'tc_config'


class TCExecutionTab(EntityView):
    __select__ = (implements('TestConfig') &
                  has_related_entities('using_config', 'object'))
    __regid__ = 'tc_execution'

    def cell_call(self, row, col):
        rset = self._cw.execute(
            'Any T,T,TB,TST,TET,TF, TS ORDERBY TST DESC WHERE '
            'T status TS, T using_config TC, T branch TB, '
            'T starttime TST, T endtime TET, T log_file TF?, '
            'TC eid %(tc)s',
            {'tc': self.cw_rset[row][col]})
        self.wview('apycot.tc.te.summarytable', rset, 'noresult')


class TCTESummaryTable(tableview.TableView):
    __select__ = implements('TestExecution')
    __regid__ = 'apycot.tc.te.summarytable'
    def call(self):
        self._cw.add_css('cubes.apycot.css')
        _ = self._cw._
        super(TCTESummaryTable, self).call(
            displayfilter=True, paginate=True,
            headers=[_('execution'), _('failures'),
                     _('branch'), _('starttime'), _('endtime'),
                     _('archive')],
            cellvids={0: 'apycot.te.statuscell',
                      1: 'apycot.te.summarycell',
                      5: 'icon'})


def available_branches(form, field):
    if form.edited_entity.environment.repository:
        return form.edited_entity.environment.repository.branches()
    return [form.edited_entity.apycot_configuration.get('branch')]

def default_branch(form):
    tc = form.edited_entity
    if tc.apycot_configuration.get('branch'):
        return tc.apycot_configuration.get('branch')
    if tc.environment.repository:
        return tc.environment.repository.default_branch()
    return None


class TCStartForm(forms.EntityFieldsForm):
    __regid__ = 'starttestform'
    __select__ = match_user_groups('managers', 'staff') & implements('TestConfig')

    form_renderer_id = 'htable'
    form_buttons = [fwdgs.SubmitButton(label=_('start test'))]
    @property
    def action(self):
        return self.edited_entity.absolute_url(vid='starttest')

    branch = ff.StringField(choices=available_branches, label=_('vcs_branch'),
                            value=default_branch)
    startrevdeps = ff.BooleanField(label=_('start_rev_deps'),
                                   value=lambda form: form.edited_entity.start_rev_deps)
    archivetestdir = ff.BooleanField(label=_('archivetestdir'), value=False)
    priority = ff.StringField(choices=[_('LOW'), _('MEDIUM'), _('HIGH')],
                              value=u'MEDIUM',
                              label=_('execution priority'),
                              sort=False, internationalizable=True)



class TCNoStartFormComponent(component.EntityVComponent):
    __regid__ = 'starttestform'
    __select__ = (component.EntityVComponent.__select__ &
                  match_user_groups('managers', 'staff') &
                  implements('TestConfig') & score_entity(lambda e: not e.all_checks))

    def cell_call(self, row, col, view=None):
        self.w(u'<div class="warning">')
        self.w(self._cw._(u'TestConfig without checkers can not be executed.'))
        self.w(u'</div>')


class TCStartFormComponent(component.EntityVComponent):
    __regid__ = 'starttestform'
    __select__ = (component.EntityVComponent.__select__ &
                  match_user_groups('managers', 'staff') &
                  implements('TestConfig') & score_entity(lambda e: e.all_checks))

    def cell_call(self, row, col, view=None):
        self.w(u'<h2>%s</h2>' % self._cw._('start tests'))
        entity = self.cw_rset.get_entity(row, col)
        form = self._cw.vreg['forms'].select('starttestform', self._cw, entity=entity)
        self.w(form.render())


class StartTestView(EntityView):
    __regid__ = 'starttest'
    __select__ = match_user_groups('managers', 'staff') & implements('TestConfig')

    def msg_url(self, msg):
        try:
            url = self._cw.build_url(self._cw.form['__redirectpath'],
                                 __message=msg)
        except KeyError:
            url = self._cw.build_url('view', vid='botstatus', __message=msg)
        return url

    def call(self):
        for i in xrange(self.cw_rset.rowcount):
            try:
                self.cell_call(i, 0)
            except Exception, ex:
                raise Redirect(self.msg_url(unicode(ex)))
        raise Redirect(self.msg_url(self._cw._('test(s) queued')))

    def cell_call(self, row, col):
        testconfig = self.cw_rset.get_entity(row, col)
        if not testconfig.all_checks:
            raise ValueError("%s config have no checker to run" % testconfig.dc_title())
        bot = bot_proxy(self._cw.vreg.config, self._cw.data)
        full_pyro_id = ':%(pyro-ns-group)s.%(pyro-instance-id)s' % self._cw.vreg.config
        bot.queue_task(testconfig.environment.name, testconfig.name,
                       cwinstid=full_pyro_id,
                       branch=self._cw.form.get('branch'),
                       priority=self._cw.form['priority'],
                       start_rev_deps=bool(self._cw.form.get('startrevdeps')),
                       archive=bool(self._cw.form.get('archivetestdir')))


class TCInContextTextView(baseviews.InContextTextView):
    __select__ = implements('TestConfig')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(entity.name)


class TCOutOfContextTextView(baseviews.OutOfContextTextView):
    __select__ = implements('TestConfig')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(entity.dc_title())


# TestExecution ################################################################

class TESummaryTable(tableview.TableView):
    __select__ = none_rset() | implements('TestExecution')
    __regid__ = 'apycot.te.summarytable'

    title = _('Apycot executions')
    category = 'startupview'

    def call(self):
        self._cw.add_css('cubes.apycot.css')
        _ = self._cw._
        if self.cw_rset is None:
            self.cw_rset = self._cw.execute(
            'Any T,TC,T,TB,TST,TET,TF, TS ORDERBY TST DESC WHERE '
            'T status TS, T using_config TC, T branch TB, '
            'T starttime TST, T endtime TET, T log_file TF?')
            self.w('<h1>%s</h1>' % _(self.title))
        super(TESummaryTable, self).call(
                   displayfilter=True, paginate=True,
                   headers=[_('execution'), _('configuration'), _('checks'),
                            _('branch'), _('starttime'), _('endtime'),
                            _('archive')],
                   cellvids={0: 'apycot.te.statuscell',
                             2: 'apycot.te.summarycell',
                             6: 'icon',
                             })


_pvs.tag_attribute(('TestExecution', 'log'), 'hidden')
_pvs.tag_subject_of(('TestExecution', 'using_revision', '*'), 'hidden')
_pvs.tag_subject_of(('TestExecution', 'using_config', '*'), 'hidden')
_pvs.tag_subject_of(('TestExecution', 'log_file', '*'), 'hidden')
_pvs.tag_object_of(('*', 'during_execution', '*'), 'hidden')


class TestExecutionPrimaryView(tabs.TabbedPrimaryView):
    __select__ = implements('TestExecution')

    default_tab = 'te_setup'
    @property
    def tabs(self):
        tabs = [_('te_setup')]
        entity = self.cw_rset.get_entity(self.cw_row or 0, self.cw_col or 0)
        for checkname in entity.configuration.all_checks:
            check = entity.check_result_by_name(checkname)
            if check is None:
                continue
            label = u'%s [<b class="status_%s">%s</b>]' % (
                xml_escape(check.name), check.status, self._cw._(check.status))
            tabs.append((anchor_name(check.name),
                         {'vid': 'te_execs', 'label': label,
                          'rset': check.as_rset()}))
        return tabs

    def render_entity_title(self, entity):
        self._cw.add_css('cubes.apycot.css')
        title = self._cw._('Execution of %(config)s#%(branch)s') % {
            'config': entity.configuration.view('outofcontext'),
            'branch': entity.branch and xml_escape(entity.branch)}
        self.w('<h1>%s</h1>' % title)


class TEConfigTab(InfoLogMixin, tabs.PrimaryTab):
    __regid__ = 'te_setup'
    __select__ = implements('TestExecution')

    def display_version_configuration(self, entity):
        title = self._cw._('version configuration')
        try:
            rset = self._cw.execute(
                'Any R, REV, B ORDERBY RN '
                'WHERE TE using_revision REV, TE eid %(te)s, '
                'REV from_repository R, REV branch B, R path RN',
                {'te': entity.eid})
        except Unauthorized:
            return # user can't read repositories for instance
        self.wview('table', rset, 'null', title=title, divid='vc%s'%entity.eid)

    def render_entity_relations(self, entity):
        self.display_version_configuration(entity)
        self.display_info_section(entity)
        self.display_log_section(entity)


class TECheckResultsTab(InfoLogMixin, tabs.PrimaryTab):
    __regid__ = 'te_execs'
    __select__ = implements('CheckResult')

    def render_entity_relations(self, entity):
        self.display_info_section(entity)
        self.display_log_section(entity)


class TEBreadCrumbTextView(ibreadcrumbs.BreadCrumbTextView):
    __select__ = implements('TestExecution')
    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(entity.printable_value('starttime'))


class TEInContextTextView(baseviews.InContextTextView):
    __select__ = implements('TestExecution')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(self._cw._('Execution on %(date)s') % {
            'date': entity.printable_value('starttime')})


class TEOutOfContextTextView(baseviews.OutOfContextTextView):
    __select__ = implements('TestExecution')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(entity.dc_title())

class TEStatusCell(TCDescriptionMixIn, tabs.PrimaryTab):
    __select__ = implements('TestExecution')
    __regid__ = 'apycot.te.statuscell'
    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(tags.a(entity.status, href=entity.absolute_url(),
                      klass="global status_%s" % entity.status,
                      title=self._cw._('see detailed execution report')))

class TESummaryCell(TCDescriptionMixIn, tabs.PrimaryTab):
    __select__ = implements('TestExecution')
    __regid__ = 'apycot.te.summarycell'
    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        checks = []
        for checkname in entity.configuration.all_checks:
            check = entity.check_result_by_name(checkname)
            if check is None or check.status == 'success':
                continue
            content = u'%s (%s)' % (self._cw._(checkname), check.status)
            url = entity.absolute_url(tab=anchor_name(checkname))
            title = self._cw._('see execution report for %s') % checkname
            checks.append(tags.a(content, href=url, title=title))
        if checks:
            self.w(u', '.join(checks))


class TEDownloadBox(box.EntityBoxTemplate):
    __regid__ = 'apycot.te.download_box'
    __select__ = (box.EntityBoxTemplate.__select__ & implements('TestExecution') &
                  score_entity(lambda x: x.log_file))

    def cell_call(self, row, col, **kwargs):
        archive = self.cw_rset.get_entity(row, col).log_file[0]
        idownloadable.download_box(self.w, archive,
                                   self._cw._('download execution environment'))


# CheckResult ##################################################################

_pvs.tag_attribute(('CheckResult', 'name'), 'hidden')
_pvs.tag_attribute(('CheckResult', 'status'), 'hidden')
_pvs.tag_attribute(('CheckResult', 'log'), 'hidden')
_pvs.tag_subject_of(('CheckResult', 'during_execution', '*'), 'hidden')
_pvs.tag_object_of(('*', 'for_check', '*'), 'hidden')


class CheckResultPrimaryView(TECheckResultsTab):
    __regid__ = 'primary'
    __select__ = implements('CheckResult')

    def render_entity_title(self, entity):
        self._cw.add_css('cubes.apycot.css')
        self.w('<h4 id="%s" >%s [<span class="status_%s">%s</span>]</h4>'
               % (anchor_name(entity.name),
                  xml_escape(entity.name), entity.status, entity.status))

