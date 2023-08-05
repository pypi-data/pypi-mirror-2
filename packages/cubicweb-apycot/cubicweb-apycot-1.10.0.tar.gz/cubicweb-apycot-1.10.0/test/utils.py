from cubicweb.devtools.testlib import CubicWebTC
from datetime import datetime

from cubes.apycot import entities

class MockProxy(object):
    def __init__(self):
        self.queued = []
    def queue_task(self, *args, **kwargs):
        self.queued.append( (args, kwargs) )
    def get_archive(self, *args, **kwargs):
        return 'hop'

proxy = MockProxy()
def bot_proxy(config, cache):
    return proxy
entities.bot_proxy = bot_proxy

class ApycotBaseTC(CubicWebTC):

    def setup_database(self):
        req = self.request()
        self.lgce = req.create_entity(
            'ProjectEnvironment', name=u'lgce',
            check_preprocessors=u'install=setup_install',
            vcs_repository_type=u'hg',
            vcs_repository=u'http://www.logilab.org/src/logilab/common',
            check_config=u'env-option=value'
            )
        self.pyp = req.create_entity('TestConfigGroup', name=u'PYTHONPACKAGE',
                                   checks=u'python_pkg,pkg_doc,python_syntax,'
                                   'python_lint,python_unittest,python_test_coverage',
                                   check_config=u'python_lint_treshold=7\n'
                                   'python_lint_ignore=thirdparty\n'
                                   'python_test_coverage_treshold=70\n')
        self.lgc = self.add_test_config(u'lgc', env=self.lgce, group=self.pyp)
        self.repo.threaded_task = lambda func: func() # XXX move to cw


    def add_test_config(self,
                        name, checks=u'python_lint,python_unittest,python_test_coverage',
                        check_config=u'python_lint_treshold=8\npouet=5',
                        env=None, group=None, **kwargs):
        """add a TestConfig instance"""
        req = self.request()
        tc = req.create_entity('TestConfig', name=name, checks=checks,
                               check_config=check_config, **kwargs)
        if group is not None:
            tc.set_relations(use_group=group)
        if env is not None:
            tc.set_relations(use_environment=env)
        return tc


    def add_execution(self, confname, check_defs, setend=True):
        """add a TestExecution instance"""
        req = self.request()
        ex = req.create_entity('TestExecution', starttime=datetime.now())
        req.execute('SET X using_config Y WHERE X eid %(x)s, Y name %(confname)s',
                    {'x': ex.eid, 'confname': confname})
        for name, status in check_defs:
            cr = req.create_entity('CheckResult', name=unicode(name), status=unicode(status))
            req.execute('SET X during_execution Y WHERE X eid %(x)s, Y is TestExecution',
                        {'x': cr.eid})
        if setend:
            req.execute('SET X endtime %(et)s WHERE X eid %(x)s',
                        {'et': datetime.now(), 'x': ex.eid})
        return ex
