# register severity sorting registered procedure
from rql.utils import register_function, FunctionDescr


class severity_sort_value(FunctionDescr):
    supported_backends = ('postgres', 'sqlite',)
    rtype = 'Int'

try:
    register_function(severity_sort_value)
except AssertionError:
    pass


options = (
    ('bot-pyro-id',
     {'type' : 'string',
      'default' : ':apycot.apycotbot',
      'help': ('Identifier of the apycot bot in the pyro name-server.'),
      'group': 'apycot', 'level': 1,
      }),
    ('bot-pyro-ns',
     {'type' : 'string',
      'default' : None,
      'help': ('Pyro name server\'s host where the bot is registered. If not '
               'set, will be detected by a broadcast query. You can also '
               'specify a port using <host>:<port> notation.'),
      'group': 'apycot', 'level': 1,
      }),
    )

try:
    from cubicweb.server import SQL_CONNECT_HOOKS
except ImportError: # no server installation
    pass
else:

    def init_sqlite_connexion(cnx):
        def severity_sort_value(text):
            return {"DEBUG": 0, "INFO": 10, "WARNING": 20,
                    "ERROR": 30, "FATAL": 40}[text]
        cnx.create_function("SEVERITY_SORT_VALUE", 1, severity_sort_value)

    sqlite_hooks = SQL_CONNECT_HOOKS.setdefault('sqlite', [])
    sqlite_hooks.append(init_sqlite_connexion)


    options += (
        ('test-master',
         {'type' : 'yn',
          'default' : True,
          'help': ('Is the repository responsible to automatically start test? '
                   'You should say yes unless you use a multiple repositories '
                   'setup, in which case you should say yes on one repository, '
                   'no on others'),
          'group': 'apycot', 'level': 1,
          }),
        ('test-exec-cleanup-delay',
         {'type' : 'time',
          'default' : '60d',
          'help': ('Interval of time after which test execution can be '
                   'deleted. Default to 60 days. Set it to 0 if you don\'t '
                   'want automatic deletion.'),
          'group': 'apycot', 'level': 1,
          }),
        )
