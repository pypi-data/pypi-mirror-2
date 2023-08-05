"""apycot cube's specific schema

:organization: Logilab
:copyright: 2008-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
__docformat__ = "restructuredtext en"
_ = unicode

from yams.buildobjs import (EntityType, RelationDefinition, String, Int,
                            Datetime, Boolean)
from yams.reader import context

from cubicweb.schema import (RQLConstraint, RRQLExpression, RQLUniqueConstraint,
                             make_workflowable)

# tracker extension ############################################################

if 'Project' in context.defined:

    class has_apycot_environment(RelationDefinition):
        __permissions__ = {
            'read':   ('managers', 'users', 'guests'),
            'add':    ('managers', 'staff',
                       RRQLExpression('U has_update_permission S', 'S'),),
            'delete': ('managers', 'staff',
                       RRQLExpression('U has_update_permission S', 'S'),),
            }
        subject = 'Project'
        object = 'ProjectEnvironment'
        cardinality = '*?'
        composite = 'subject'

    CONF_WRITE_GROUPS = ('managers', 'staff')

else:

    CONF_WRITE_GROUPS = ('managers', )


# nosylist extension ###########################################################

if 'nosy_list' in context.defined:

    class interested_in(RelationDefinition):
        '''users to notify of changes concerning this entity'''
        subject = 'CWUser'
        object = ('ProjectEnvironment', 'TestConfig')

    class nosy_list(RelationDefinition):
        subject = ('ProjectEnvironment', 'TestConfig', 'TestExecution')
        object = 'CWUser'


# configuration entities and relations #########################################

def post_build_callback(schema):
    if not 'apycot' in schema['Repository'].permissions['read']:
        schema['Repository'].permissions['read'] += ('apycot',)
    # XXX has to be in post_build_callback since forge overwrite File
    # permissions
    if not 'apycot' in schema['File'].permissions['add']:
        schema['File'].permissions['add'] += ('apycot',)


class ProjectEnvironment(EntityType):
    __permissions__ = {
        'read':   ('managers', 'users', 'guests', 'apycot'),
        'add':    CONF_WRITE_GROUPS,
        'update': CONF_WRITE_GROUPS,
        'delete': CONF_WRITE_GROUPS,
        }

    name = String(
        required=True, unique=True, maxsize=128,
        description=_('name for this environment')
        )

    vcs_repository_type = String(
        required=True,
        vocabulary=(u'hg', u'svn', u'cvs', u'fs'),
        description=_('kind of version control system (vcs): hg (mercurial), '
                      'svn (subversion), cvs (CVS), fs (file system, eg no '
                      'version control)')
        )
    vcs_repository = String(
        required=True,
        description=_('path or url to the vcs repository containing the project')
        )
    vcs_path = String(
        description=_('relative path to the project into the repository')
        )

    check_preprocessors = String(
        description=_('preprocessors to use for this project for install, '
                      'debian, build_doc... (one per line)'),
        fulltextindexed=True
        )
    check_environment = String(
        description=_('environment variables to be set in the check process '
                      'environment (one per line)'),
        fulltextindexed=True
        )
    check_config = String(
        description=_('preprocessor/checker options (one per line)'),
        fulltextindexed=True
        )


class TestConfigGroup(EntityType):
    """regroup some common configuration used by multiple projects"""
    __permissions__ = {
        'read':   ('managers', 'users', 'guests', 'apycot'),
        'add':    CONF_WRITE_GROUPS,
        'update': CONF_WRITE_GROUPS,
        'delete': CONF_WRITE_GROUPS,
        }

    name = String(
        required=True, unique=True, maxsize=128,
        description=_('name for this configuration group'),
        )
    checks = String(
        description=_('comma separated list of checks to execute in this test config'),
        fulltextindexed=True
        )
    check_environment = String(
        description=_('environment variables to be set in the test process '
                      'environment (one per line)'),
        fulltextindexed=True
        )
    check_config = String(
        description=_('preprocessor/checker options (one per line)'),
        fulltextindexed=True
        )


class TestConfig(TestConfigGroup):
    """apycot configuration to register a project branch to test"""
    __permissions__ = {
        'read':   ('managers', 'users', 'guests', 'apycot'),
        'add':    CONF_WRITE_GROUPS,
        'update': CONF_WRITE_GROUPS,
        'delete': CONF_WRITE_GROUPS,
        }
    name = String(
        override=True, required=True, maxsize=128, indexed=True,
        description=_('name for this configuration'),
        constraints=[RQLUniqueConstraint('S name N, S use_environment E, '
                                         'Y use_environment E, Y name N', 'Y')]
        )

    start_mode = String(
        required=True, indexed=True,
        vocabulary=(_('manual'), _('on new revision'),
                    _('hourly'), _('daily'),_('weekly'), _('monthly')),
        default='manual',
        description=_('when this test config should be started')
        )
    start_rev_deps = Boolean(
        default=False,
        description=_("should tests for project environment depending on this "
                      "test's environment be started when this test is "
                      "automatically triggered")
        )
    # simply use 'branch=XXX' in check_config field. Get back documentation
    # before to remove code below
    # vcs_branch  = String(
    #     description=_('branch to use for test\'s checkout. In case of '
    #                   'subversion repository, this should be the relative path '
    #                   'of the branch into the repository (vcs_path won\'t be '
    #                   'considered then).'),
    #     maxsize=256
    #     )
    subpath = String(
        description=_('path relative to the checkout directory to be considered by tests')
        )

make_workflowable(TestConfig, in_state_descr=_('automatic test status'))


class use_environment(RelationDefinition):
    __permissions__ = {
        'read':   ('managers', 'users', 'guests', 'apycot'),
        'add':    CONF_WRITE_GROUPS,
        'delete': CONF_WRITE_GROUPS,
        }
    inlined = True
    subject = 'TestConfig'
    object = 'ProjectEnvironment'
    cardinality = '1*'
    composite = 'object'
    description=_('project environment in which this test config should be launched')
    constraints = [RQLUniqueConstraint('S name N, Y use_environment O, Y name N', 'Y')]


class local_repository(RelationDefinition):
    __permissions__ = {
        'read':   ('managers', 'users', 'guests', 'apycot'),
        'add':    CONF_WRITE_GROUPS,
        'delete': CONF_WRITE_GROUPS,
        }
    subject = 'ProjectEnvironment'
    object = 'Repository'
    cardinality = '?*'
    description = _('link to a vcsfile repository, may be used to replace '
                    'vcs_repository_type / vcs_repository to have deeper '
                    'integration.')


class needs_checkout(RelationDefinition):
    __permissions__ = {
        'read':   ('managers', 'users', 'guests', 'apycot'),
        'add':    CONF_WRITE_GROUPS,
        'delete': CONF_WRITE_GROUPS,
        }
    subject = ('ProjectEnvironment', 'TestConfig')
    object = 'ProjectEnvironment'
    description = _('project\'s environments that should be installed from '
                    'their repository to execute test with this configuration')
    #constraints=[RQLConstraint('NOT S identity O')]


class use_group(RelationDefinition):
    __permissions__ = {
        'read':   ('managers', 'users', 'guests',),
        'add':    CONF_WRITE_GROUPS,
        'delete': CONF_WRITE_GROUPS,
        }
    subject = ('TestConfig', 'TestConfigGroup')
    object = 'TestConfigGroup'
    #constraints=[RQLConstraint('NOT S identity O')]


# execution data entities and relations ########################################

BOT_ENTITY_PERMS = {
        'read':   ('managers', 'users', 'guests', 'apycot'),
        'add':    ('apycot',),
        'update': ('apycot',),
        'delete': ('managers',),
        }
BOT_RELATION_PERMS = {
        'read':   ('managers', 'users', 'guests', 'apycot'),
        'add':    ('apycot',),
        'delete': ('managers',),
        }

class TestExecution(EntityType):
    __permissions__ = BOT_ENTITY_PERMS
    status = String(required=True, internationalizable=True, indexed=True,
                    default=u'set up',
                    vocabulary=(_('set up'), _('running tests'),
                                _('success'), _('partial'),
                                _('failure'), _('error'), _('nodata'),
                                _('missing'), _('skipped'),
                                _('killed'))
                    )
    starttime = Datetime(required=True)
    endtime   = Datetime()
    branch = String(indexed=True)
    log = String()


class CheckResult(EntityType):
    """group results of execution of a specific test on a project"""
    __permissions__ = BOT_ENTITY_PERMS

    name      = String(required=True, indexed=True, maxsize=128, description=_('check name'))
    status    = String(required=True,
                       vocabulary=(_('success'), _('partial'),
                                   _('failure'), _('error'), _('nodata'),
                                   _('missing'), _('skipped'),
                                   _('killed'), _('processing'))
                       )
    starttime = Datetime()
    endtime   = Datetime()
    log = String()


class CheckResultInfo(EntityType):
    """arbitrary information about execution of a specific test on a project"""
    __permissions__ = BOT_ENTITY_PERMS

    type = String(internationalizable=True, indexed=True)
    label = String(required=True, internationalizable=True)
    value = String(required=True, internationalizable=True)


class using_config(RelationDefinition):
    __permissions__ = BOT_RELATION_PERMS
    inlined = True
    subject = 'TestExecution'
    object = 'TestConfig'
    cardinality = '1*'
    composite = 'object'


class during_execution(RelationDefinition):
    __permissions__ = BOT_RELATION_PERMS
    inlined = True
    subject = 'CheckResult'
    object = 'TestExecution'
    cardinality = '1*'
    composite = 'object'


class for_check(RelationDefinition):
    __permissions__ = BOT_RELATION_PERMS
    inlined = True
    subject = 'CheckResultInfo'
    object = ('CheckResult', 'TestExecution')
    cardinality = '1*'
    composite = 'object'


class using_revision(RelationDefinition):
    __permissions__ = BOT_RELATION_PERMS
    subject = 'TestExecution'
    object = 'Revision'
    description = _('link to revision which has been used in the test '
                    'environment for configurations which are linked to a '
                    'repository.')


class log_file(RelationDefinition):
    __permissions__ = BOT_RELATION_PERMS
    subject = 'TestExecution'
    object = 'File'
    cardinality = '??'
    composite = 'subject'
