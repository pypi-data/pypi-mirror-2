"""this module contains the cube-specific entities' classes

:organization: Logilab
:copyright: 2008-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
:license: General Public License version 2 - http://www.gnu.org/licenses
"""

__docformat__ = "restructuredtext en"

from logilab.common.decorators import cached
from logilab.common.textutils import TIME_UNITS, BYTE_UNITS, apply_units, splitstrip
from logilab.mtconverter import xml_escape

from cubicweb.interfaces import IPrevNext
from cubicweb.entity import _marker
from cubicweb.entities import AnyEntity, fetch_config

try:
    from cubes.nosylist.interfaces import INosyList
except ImportError:
    INosyList = None


def text_to_dict(text):
    """parse multilines text containing simple 'key=value' lines and return a
    dict of {'key': 'value'}. When the same key is encountered multiple time,
    value is turned into a list containing all values.

    >>> text_to_dict('''multiple=1
    ... multiple= 2
    ... single =3
    ... ''')
    {'single': '3', 'multiple': ['1', '2']}

    """
    res = {}
    if not text:
        return res
    for line in text.splitlines():
        line = line.strip()
        if line:
            key, value = [w.strip() for w in line.split('=', 1)]
            if key in res:
                try:
                    res[key].append(value)
                except AttributeError:
                    res[key] = [res[key], value]
            else:
                res[key] = value
    return res

def vcsrepo_apycot_info(repo):
    if repo.type == 'mercurial':
        return 'hg', repo.path
    return 'svn', repo.path

class ExecutionRSSMixin(object):

    RSS_LIMIT = 20

    def rss_label(self, vid='rss'):
        if vid == 'rss':
            return self._cw._(u'rss_exec_button')
        elif vid == 'changes_rss':
            return self._cw._(u'changes_rss_exec_button')
        else:
            assert False, 'unknow vid %s' % vid

    def rss_description(self, vid):
        raise NotImplementedError()

    def rss_rql(self, vid):
        raise NotImplementedError()


class ProjectEnvironment(AnyEntity, ExecutionRSSMixin):
    __regid__ = 'ProjectEnvironment'

    if INosyList is not None:
        __implements__ = AnyEntity.__implements__ + (INosyList,)

    fetch_attrs, fetch_order = fetch_config(['name'])

    def parent(self):
        """hierarchy, used for breadcrumbs"""
        try:
            return self.reverse_has_apycot_environment[0]
        except (AttributeError, IndexError):
            return None

    def printable_value(self, attr, value=_marker, attrtype=None,
                        format='text/html', displaytime=True):
        """return a displayable value (i.e. unicode string) which may contains
        html tags
        """
        attr = str(attr)
        if value is _marker:
            value = getattr(self, attr)
        if value is None or value == '': # don't use "not", 0 is an acceptable value
            return u''
        if attr == 'vcs_path' and format == 'text/html':
            if '://' in value:
                return '<a href="%s">%s</a>' % (xml_escape(value),
                                                xml_escape(value))
            return xml_escape(value)
        return super(ProjectEnvironment, self).printable_value(
            attr, value, attrtype, format, displaytime)
    # rss related methods #####################################################


    def rss_description(self, vid='rss'):
        data = {
            'pe': self.dc_title(),
            }
        if vid == 'rss':
            return self._cw._('Subscribe to all executions on %(pe)s') % data
        elif vid == 'changes_rss':
            return self._cw._('Subscribe to all changes of %(pe)s') % data
        else:
            assert False, 'unknow vid %s' % vid

    def rss_rql(self, vid='rss'):
        return 'TestExecution TE ORDERBY SD DESC LIMIT %i WHERE TE using_config TC, TE starttime SD, TC use_environment PE, PE eid %i'\
               % (self.RSS_LIMIT, self.eid)

    # cube specific logic #####################################################

    @property
    def repository(self):
        return self.local_repository and self.local_repository[0] or None

    def dependencies(self, _done=None):
        if _done is None:
            _done = set()
        _done.add(self.eid)
        result = []
        for pe in self.needs_checkout:
            if pe.eid in _done:
                continue
            result.append(pe)
            result += pe.dependencies(_done)
        return result

    # apycot bot helpers #######################################################

    @property
    def my_apycot_process_environment(self):
        return text_to_dict(self.check_environment)

    @property
    def my_apycot_configuration(self):
        return text_to_dict(self.check_config)

    @property
    def apycot_configuration(self):
        return self.my_apycot_configuration

    @property
    def apycot_preprocessors(self):
        return text_to_dict(self.check_preprocessors)

    @property
    def apycot_repository_def(self):
        if self.vcs_repository:
            vcsrepo = self.vcs_repository
            vcsrepotype = self.vcs_repository_type
        elif self.repository:
            vcsrepotype, vcsrepo = vcsrepo_apycot_info(self.repository)
        else:
            vcsrepo = vcsrepotype = None
        repo_def = {
            'repository_type': vcsrepotype,
            'repository': vcsrepo,
            'path': self.vcs_path
            }
        if 'branch' in self.apycot_configuration:
            repo_def['branch'] = self.apycot_configuration['branch']
        return repo_def


    # tracker integration ######################################################

    @property
    def project(self):
        if 'has_apycot_environment' in self._cw.vreg.schema:
            return self.reverse_has_apycot_environment[0]


class TestConfigGroup(AnyEntity):
    __regid__ = 'TestConfigGroup'

    fetch_attrs, fetch_order = fetch_config(['name', 'checks'])

    def config_parts(self, _done=None):
        if _done is None:
            _done = set()
        _done.add(self.eid)
        result = [self]
        for group in self.use_group:
            if group.eid in _done:
                continue
            result += group.config_parts(_done)
        return result
    config_parts = cached(config_parts, keyarg=0)

    @property
    def all_checks(self):
        try:
            return self.all_checks_and_owner()[1]
        except TypeError:
            return None

    def all_checks_and_owner(self):
        for group in self.config_parts():
            if group.checks:
                return group, splitstrip(group.checks)

    def _regroup_dict(self, prop, regroup=None):
        if regroup is None:
            regroup = {}
        for group in reversed(self.config_parts()):
            regroup.update(getattr(group, prop))
        return regroup

    # apycot bot helpers #######################################################

    @property
    def my_apycot_process_environment(self):
        return text_to_dict(self.check_environment)

    @property
    def apycot_process_environment(self):
        return self._regroup_dict('my_apycot_process_environment')

    @property
    def my_apycot_configuration(self):
        return text_to_dict(self.check_config)

    @property
    def apycot_configuration(self):
        return self._regroup_dict('my_apycot_configuration')

    # XXX for 1.4 migration
    @property
    def apycot_preprocessors(self):
        return text_to_dict(self.check_preprocessors)


class TestConfig(TestConfigGroup, ExecutionRSSMixin):
    __regid__ = 'TestConfig'

    if INosyList is not None:
        __implements__ = AnyEntity.__implements__ + (INosyList,)


    def dc_title(self):
        return '%s / %s' % (self.environment.name, self.name)

    def parent(self):
        return self.environment

    def rest_path(self, use_ext_eid=False):
        return u'%s/%s' % (self.environment.rest_path(),
                           self._cw.url_quote(self.name))


    # rss related methods #####################################################

    def rss_description(self, vid='rss'):
        data = {
            'conf': self.dc_title(),
            }
        if vid == 'rss':
            return self._cw._('Subscribe to all executions of %(conf)s') % data
        elif vid == 'changes_rss':
            return self._cw._('Subscribe to all changes of %(conf)s') % data
        else:
            assert False, 'unknow vid %s' % vid

    def rss_rql(self, vid='rss'):
        return 'TestExecution TE ORDERBY SD DESC LIMIT %i WHERE TE using_config TC, TE starttime SD, TC eid %i'\
               % (self.RSS_LIMIT, self.eid)

    # cube specific logic #####################################################

    @property
    def environment(self):
        return self.use_environment[0]

    def dependencies(self):
        _done = set()
        result = self.environment.dependencies(_done)
        for dpe in self.needs_checkout:
            if dpe.eid in _done:
                continue
            result.append(dpe)
            result += dpe.dependencies(_done)
        return result

    @cached
    def all_check_results(self):
        rset = self._cw.execute('Any MAX(X), XN GROUPBY XN, EXB ORDERBY XN '
                                'WHERE X is CheckResult, X name XN, '
                                'X during_execution EX, EX using_config C, '
                                'EX branch EXB, C eid %(c)s',
                                {'c': self.eid})
        return list(rset.entities())

    def latest_execution(self):
        rset = self._cw.execute('Any X, C ORDERBY X DESC LIMIT 1'
                                'WHERE X is TestExecution, X using_config C, '
                                'C eid %(c)s', {'c': self.eid})
        if rset:
            return rset.get_entity(0, 0)

    def latest_full_execution(self):
        rset = self._cw.execute('Any X, C, COUNT(CR) GROUPBY X, C '
                                'ORDERBY 3 DESC, X DESC LIMIT 1'
                                'WHERE X is TestExecution, X using_config C, '
                                'C eid %(c)s, CR during_execution X',
                                {'c': self.eid})
        if rset:
            return rset.get_entity(0, 0)

    def latest_check_result_by_name(self, name, branch):
        for cr in self.all_check_results():
            if cr.name == name and cr.execution.branch == branch:
                return cr

    def match_branch(self, branch):
        return self.apycot_configuration.get('branch', branch) == branch

    # apycot bot helpers #######################################################

    def _regroup_dict(self, prop, with_pe=True):
        if with_pe:
            regroup = getattr(self.environment, prop).copy()
        else:
            regroup = {}
        return super(TestConfig, self)._regroup_dict(prop, regroup)

    @property
    def apycot_process_environment(self):
        return self._regroup_dict('my_apycot_process_environment')

    @property
    @cached
    def apycot_configuration(self):
        return self._apycot_configuration()

    @property
    @cached
    def apycot_tc_configuration(self):
        return self._apycot_configuration(with_pe=False)

    def _apycot_configuration(self, with_pe=True):
        config = self._regroup_dict('my_apycot_configuration', with_pe=with_pe)
        for option in (u'max-cpu-time', u'max-reprieve', u'max-time'):
            if option in config:
                config[option] = apply_units(config[option], TIME_UNITS)
        if u'max-memory' in config:
            config[u'max-memory'] = apply_units(config[u'max-memory'],
                                                BYTE_UNITS)
        return config

    # tracker integration ######################################################

    @property
    def project(self):
        """tracker integration"""
        return self.parent().project


class TestExecution(AnyEntity, ExecutionRSSMixin):
    __regid__ = 'TestExecution'
    __implements__ = AnyEntity.__implements__ + (IPrevNext,)

    def rest_path(self, use_ext_eid=False):
        return u'%s/%s' % (self.parent().rest_path(),
                           self.eid)

    @property
    def checkers(self):
        return self.reverse_during_execution

    def dc_title(self):
        return self._cw._('Execution of %(config)s on %(date)s') % {
            'config': self.configuration.dc_title(),
            'date': self.printable_value('starttime')}

    def dc_date(self, date_format=None):
        return self._cw.format_date(self.starttime, date_format=date_format)

    def parent(self):
        """hierarchy, used for breadcrumbs"""
        return self.configuration

    # IPrevNext interface #####################################################

    def previous_entity(self):
        rql = ('Any X,C ORDERBY X DESC LIMIT 1 '
               'WHERE X is TestExecution, X using_config C, C eid %(c)s, X branch %(branch)s, '
               'X eid < %(x)s')
        rset = self._cw.execute(rql, {'c': self.configuration.eid, 'x': self.eid,
                                      'branch': self.branch})
        if rset:
            return rset.get_entity(0, 0)

    def next_entity(self):
        rql = ('Any X,C ORDERBY X ASC LIMIT 1 '
               'WHERE X is TestExecution, X using_config C, C eid %(c)s, X branch %(branch)s, '
               'X eid > %(x)s')
        rset = self._cw.execute(rql, {'c': self.configuration.eid, 'x': self.eid,
                                      'branch': self.branch})
        if rset:
            return rset.get_entity(0, 0)

    # rss related methods #####################################################

    def rss_description(self, vid='rss'):
        data = {
            'conf': self.configuration.dc_title(),
            'branch': self.branch,
            }
        if vid == 'rss':
            return self._cw._('Subscribe to all executions of %(conf)s for branch %(branch)s') % data
        elif vid == 'changes_rss':
            return self._cw._('Subscribe to all changes of %(conf)s for branch %(branch)s') % data
        else:
            assert False, 'unknow vid %s' % vid

    def rss_rql(self, vid='rss'):
        if self.branch is None:
            return 'TestExecution TE ORDERBY SD DESC LIMIT %i WHERE TE using_config TC, TC eid %i, TE branch NULL, TE starttime SD'\
                   % (self.RSS_LIMIT, self.configuration.eid)
        else:
            return 'TestExecution TE ORDERBY SD DESC LIMIT %i WHERE TE using_config TC, TC eid %i, TE branch "%s", TE starttime SD'\
                   % (self.RSS_LIMIT, self.configuration.eid, self.branch)

    # cube specific logic #####################################################

    @property
    def configuration(self):
        return self.using_config[0]

    def check_result_by_name(self, name):
        for cr in self.reverse_during_execution:
            if cr.name == name:
                return cr

    @cached
    def status_changes(self):
        """return a dict containing status test changes between the previous
        execution and this one. Changes are described using a 2-uple:

          (previous status, current status)

        Return an empty dict if no previous execution is found or if nothing
        changed.
        """
        result = {}
        previous_exec = self.previous_entity()
        if previous_exec is None:
            return
        for cr in self.reverse_during_execution:
            previous_cr = previous_exec.check_result_by_name(cr.name)
            if previous_cr is not None and previous_cr.status != cr.status:
                result[cr.name] = (previous_cr, cr)
        return result

    def repository_revision(self, repository):
        for rev in self.using_revision:
            if rev.repository.eid == repository.eid:
                return rev

    # tracker integration ######################################################

    @property
    def project(self):
        return self.configuration.project


class CheckResult(AnyEntity):
    __regid__ = 'CheckResult'
    __implements__ = AnyEntity.__implements__ + (IPrevNext,)
    fetch_attrs, fetch_order = fetch_config(['starttime', 'endtime',
                                             'name', 'status'])

    def parent(self):
        """hierarchy, used for breadcrumbs"""
        return self.execution

    # IPrevNext interface #####################################################


    def absolute_url(self, *args, **kwargs):
        kwargs['tab'] = self.name
        return self.execution.absolute_url(*args, **kwargs)

    def previous_entity(self):
        previous_exec = self.execution.previous_entity()
        if previous_exec:
            return previous_exec.check_result_by_name(self.name)

    def next_entity(self):
        next_exec = self.execution.next_entity()
        if next_exec:
            return next_exec.check_result_by_name(self.name)

    # cube specific logic #####################################################

    @property
    def execution(self):
        return self.during_execution[0]


class CheckResultInfo(AnyEntity):
    __regid__ = 'CheckResultInfo'
    fetch_attrs, fetch_order = fetch_config(['type', 'label', 'value'])

    def parent(self):
        """hierarchy, used for breadcrumbs"""
        return self.for_check[0]


from logilab.common.pyro_ext import ns_get_proxy

def bot_proxy(config, cache):
    if not 'botproxy' in cache:
        cache['botproxy'] = ns_get_proxy(config['bot-pyro-id'], 'apycot',
                                         nshost=config['bot-pyro-ns'])
    return cache['botproxy']
