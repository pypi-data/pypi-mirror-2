import os
import re

from logilab.common.testlib import unittest_main

from cubicweb.devtools.testlib import MAILBOX
from cubicweb import Binary


from utils import ApycotBaseTC, proxy
from cubes.apycot.hooks import start_test # load once bot_proxy has been monkey patched


def clean_str(string):
    url_filtered = re.sub('lgc/[0-9]*', 'lgc/<EID>', string.strip())
    return re.sub('[0-9]', 'X', url_filtered)

class NotificationTC(ApycotBaseTC):

    def test_exec_status_change(self):
        self.login('apycotbot', password='apycot')
        self.add_execution('lgc', [('unittest', 'success'), ('coverage', 'success')])
        self.assertEquals(len(MAILBOX), 0)
        self.commit()
        self.assertEquals(len(MAILBOX), 0)
        self.add_execution('lgc', [('unittest', 'success'), ('coverage', 'success')])
        self.assertEquals(len(MAILBOX), 0)
        self.commit()
        self.assertEquals(len(MAILBOX), 0)
        self.add_execution('lgc', [('unittest', 'failure'), ('coverage', 'failure')])
        self.assertEquals(len(MAILBOX), 0)
        self.commit()
        self.assertEquals(len(MAILBOX), 1)
        self.assertEquals(MAILBOX[0].message.get('Subject'),
                          '[data] lgce / lgc now has 2 failure')
        self.assertTextEquals(clean_str(MAILBOX[0].message.get_payload(decode=True)),
                              '''The following changes occured between executions on branch None:

* coverage status changed from success to failure
* unittest status changed from success to failure

Imported changes occured between XXXX/XX/XX XX:XX and XXXX/XX/XX XX:XX:
* no change found in known repositories

URL: http://testing.fr/cubicweb/projectenvironment/lgce/lgc/<EID>''')


    def test_exec_one_status_change(self):
        self.login('apycotbot', password='apycot')
        self.add_execution('lgc', [('unittest', 'success'), ('coverage', 'success')])
        self.commit()
        self.add_execution('lgc', [('unittest', 'failure')])
        self.commit()
        self.assertEquals(len(MAILBOX), 1)
        self.assertEquals(MAILBOX[0].message.get('Subject'),
                          '[data] lgce / lgc: success -> failure (unittest)')
        self.assertTextEquals(clean_str(MAILBOX[0].message.get_payload(decode=True)),
                              '''The following changes occured between executions on branch None:

* unittest status changed from success to failure

Imported changes occured between XXXX/XX/XX XX:XX and XXXX/XX/XX XX:XX:
* no change found in known repositories

URL: http://testing.fr/cubicweb/projectenvironment/lgce/lgc/<EID>''')


def setup_module(*args, **kwargs):
    if not os.path.exists('data/hgrepo'):
        os.mkdir('data/hgrepo')
        os.system('cd data/hgrepo; hg init;')

def teardown_module(*args, **kwargs):
    if os.path.exists('data/hgrepo'):
        os.system('rm -rf data/hgrepo')


class StartTestTC(ApycotBaseTC):

    def grant_write_perm(self, repo, group):
        req = self.request()
        managers = req.execute('CWGroup G WHERE G name %(group)s',
                               {'group': group}).get_entity(0, 0)
        req.create_entity(
            'CWPermission', name=u"write", label=u'repo x write perm',
            reverse_require_permission=repo,
            require_group=managers)

    def test_new_vc_trigger(self):
        self.lgc.set_attributes(start_mode=u'on new revision')
        lgc2 = self.add_test_config(u'lgc2', start_mode=u'manual', env=self.lgce)
        lgc3 = self.add_test_config(u'lgc3', start_mode=u'on new revision',
                                    check_config=u'branch=stable', env=self.lgce)
        lgce2 = self.request().create_entity(
            'ProjectEnvironment', name=u'lgce2',
            check_preprocessors=u'install=setup_install',
            vcs_repository_type=u'hg',
            vcs_repository=u'http://www.logilab.org/src/logilab/common',
            vcs_path=u'dir1',
            )
        lgc4 = self.add_test_config(u'lgc4', start_mode=u'on new revision',
                                    check_config=u'branch=default',
                                    env=lgce2, start_rev_deps=True)
        lgc5 = self.add_test_config(u'lgc5', start_mode=u'manual',
                                    env=lgce2)
        self.commit()
        r = self.request().create_entity('Repository', path=u'data/hgrepo', type=u'mercurial', encoding=u'utf8')
        self.execute('SET PE local_repository R WHERE PE is ProjectEnvironment, R is Repository')
        self.grant_write_perm(r, 'managers')
        self.commit()
        # now test
        r.vcs_add(u'dir1', u'tutu.png', Binary('data'))
        self.commit()
        self.assertEquals(sorted(proxy.queued),
                          # data is the pyro instance id
                          [(('lgce', 'lgc'), {'cwinstid': ':cubicweb.data',
                                              'branch': 'default',
                                              'start_rev_deps': False}),
                           (('lgce2', 'lgc4'), {'cwinstid': ':cubicweb.data',
                                                'branch': 'default',
                                                'start_rev_deps': True})])
        proxy.queued = []
        r.vcs_add(u'dir1', u'tutu.png', Binary('data'), branch=u'stable')
        self.commit()
        self.assertEquals(proxy.queued, [(('lgce', 'lgc'), {'cwinstid': ':cubicweb.data',
                                                            'branch': 'stable',
                                                            'start_rev_deps': False}),
                                         (('lgce', 'lgc3'), {'cwinstid': ':cubicweb.data',
                                                             'branch': 'stable',
                                                             'start_rev_deps': False})])
        proxy.queued = []
        r.vcs_add(u'dir2', u'tutu.png', Binary('data'))
        self.commit()
        self.assertEquals(proxy.queued, [(('lgce', 'lgc'), {'cwinstid': ':cubicweb.data',
                                                            'branch': 'default',
                                                            'start_rev_deps': False})])

    def test_datetime_trigger(self):
        self.lgc.set_attributes(start_mode=u'hourly')
        lgc2 = self.add_test_config(u'lgc2', start_mode=u'hourly', env=self.lgce)
        lgce2 = self.request().create_entity(
            'ProjectEnvironment', name=u'lgce2',
            check_preprocessors=u'install=setup_install',
            vcs_repository_type=u'hg',
            vcs_repository=u'http://www.logilab.org/src/logilab/common',
            vcs_path=u'dir1',
            )
        lgc3 = self.add_test_config(u'lgc3', start_mode=u'hourly',
                                    check_config=u'branch=default',
                                    env=lgce2, start_rev_deps=True)
        r = self.request().create_entity('Repository', path=u'data/hgrepo', type=u'mercurial', encoding=u'utf8')
        self.grant_write_perm(r, 'managers')
        r.vcs_add(u'dir1', u'tutu.png', Binary('data'))
        self.execute('SET PE local_repository R WHERE PE name "lgce2"')
        self.commit()
        session = self.session
        session.set_pool()
        self.assertEquals(start_test(session, 'daily'),
                          set())
        self.assertEquals(start_test(session, 'hourly'),
                          set((('lgce', 'lgc', False, None),
                               ('lgce', 'lgc2', False, None),
                               ('lgce2', 'lgc3', True, 'default')))
                          )
        lgc2.fire_transition('deactivate')
        self.commit()
        session.set_pool()
        self.assertEquals(start_test(session, 'hourly'),
                          set((('lgce', 'lgc', False, None),
                               ('lgce2', 'lgc3', True, 'default')))
                          )
        self.login('apycotbot', password='apycot')
        ex = self.add_execution('lgc3', (), setend=True)
        ex.set_relations(using_revision=r.branch_head())
        self.commit()
        self.restore_connection()
        session.set_pool()
        self.assertEquals(start_test(session, 'hourly'),
                          set((('lgce', 'lgc', False, None),))
                          )

if __name__ == '__main__':
    unittest_main()
