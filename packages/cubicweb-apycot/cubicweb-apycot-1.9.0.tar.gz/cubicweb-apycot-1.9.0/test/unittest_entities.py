from logilab.common.testlib import unittest_main

from cubicweb import ValidationError

from utils import ApycotBaseTC


class MockWriter(object):
    """fake apycot.IWriter class, ignore every thing"""

    def skip(self, *args, **kwargs):
        pass
    def _debug(self, *args, **kwargs):
        print args, kwargs
    __init__= skip
    raw = log = execution_info = skip
    start_test = start_check = end_check = end_test = skip
    set_exec_status = skip


class ApycotConfigTC(ApycotBaseTC):

    def setup_database(self):
        ApycotBaseTC.setup_database(self)
        self.add_test_config(u'lgd', checks=None, check_config=None,
                             env=self.lgce, group=self.pyp)

    def test_use_group_base(self):
        lgd = self.execute('TestConfig X WHERE X name "lgd"').get_entity(0, 0)
        self.assertEquals(lgd.all_checks,
                          'python_pkg,pkg_doc,python_syntax,python_lint,python_unittest,python_test_coverage'.split(','))
        self.assertEquals(lgd.apycot_configuration,
                          {'python_lint_treshold': '7',
                           'python_lint_ignore': 'thirdparty',
                           'python_test_coverage_treshold': '70',
                           'env-option': 'value'})

    def test_use_group_override(self):
        lgc = self.execute('TestConfig X WHERE X name "lgc"').get_entity(0, 0)
        self.assertEquals(lgc.all_checks,
                          'python_lint,python_unittest,python_test_coverage'.split(','))
        self.assertEquals(lgc.apycot_configuration,
                          {'python_lint_treshold': '8',
                           'python_lint_ignore': 'thirdparty',
                           'python_test_coverage_treshold': '70',
                           'pouet': '5',
                           'env-option': 'value'})

    def test_latest_full_execution(self):
        self.login('apycotbot', password='apycot')
        ex1 = self.add_execution('lgc', [('unittest', 'success'), ('coverage', 'success')])
        ex2 = self.add_execution('lgc', [('unittest', 'failure')])
        self.commit()
        self.restore_connection()
        self.assertEquals(self.lgc.latest_execution().eid, ex2.eid)
        self.assertEquals(self.lgc.latest_full_execution().eid, ex1.eid)

    def test_all_check_results(self):
        self.login('apycotbot', password='apycot')
        ex1 = self.add_execution('lgc', [('unittest', 'success'), ('coverage', 'success')])
        covcr = ex1.check_result_by_name('coverage').eid
        ex2 = self.add_execution('lgc', [('unittest', 'failure')])
        ucr = ex2.check_result_by_name('unittest').eid
        self.commit()
        self.restore_connection()
        self.assertEquals([cr.eid for cr in self.lgc.all_check_results()],
                          [covcr, ucr])

    def test_duplicated_tc_same_env(self):
        tcgncstrs = self.schema['TestConfigGroup'].rdef('name').constraints
        self.assertEquals([cstr.type() for cstr in tcgncstrs], ['SizeConstraint', 'UniqueConstraint'])
        tcncstrs = self.schema['TestConfig'].rdef('name').constraints
        self.assertEquals([cstr.type() for cstr in tcncstrs], ['RQLUniqueConstraint', 'SizeConstraint'])
        self.request().create_entity('TestConfig', name=u'lgd')
        self.execute('SET X use_environment Y WHERE X name "lgd", Y is ProjectEnvironment')
        self.assertRaises(ValidationError, self.commit)

    def test_status_change(self):
        self.login('apycotbot', password='apycot')
        ex1 = self.add_execution('lgc', [('unittest', 'success'), ('coverage', 'success')])
        ex2 = self.add_execution('lgc', [('unittest', 'failure'), ('coverage', 'success')])
        ex3 = self.add_execution('lgc', [('unittest', 'success'), ('coverage', 'error')])
        self.commit()

        status_changes = ex2.status_changes()
        for key, values in status_changes.iteritems():
            self.assertTrue(hasattr(values[0], 'eid'))
            self.assertTrue(hasattr(values[1], 'eid'))
            status_changes[key] = (values[0].eid, values[1].eid)
        self.assertDictEqual(status_changes,
                             {'unittest': (ex1.check_result_by_name('unittest').eid,
                                           ex2.check_result_by_name('unittest').eid)})
        status_changes = ex3.status_changes()
        for key, values in status_changes.iteritems():
            self.assertTrue(hasattr(values[0], 'eid'))
            self.assertTrue(hasattr(values[1], 'eid'))
            status_changes[key] = (values[0].eid, values[1].eid)
        self.assertDictEqual(status_changes,
                             {'unittest': (ex2.check_result_by_name('unittest').eid,
                                           ex3.check_result_by_name('unittest').eid),
                              'coverage': (ex2.check_result_by_name('coverage').eid,
                                           ex3.check_result_by_name('coverage').eid)})

    def test_branch_for_pe(self):
        #check that branch defined in ProjectEnvironement are propertly retrieved

        data = {
            'cc': self.lgce.check_config + '\nbranch=toto',
            'e': self.lgce.eid,

        }
        self.execute('SET PE check_config %(cc)s WHERE PE eid %(e)s', data)

        entity = self.execute('Any PE WHERE PE eid %(e)s', data).get_entity(0,0)

        repo_def = entity.apycot_repository_def
        self.assertIn('branch', repo_def)
        self.assertEquals(repo_def['branch'], 'toto')


if __name__ == '__main__':
    unittest_main()
