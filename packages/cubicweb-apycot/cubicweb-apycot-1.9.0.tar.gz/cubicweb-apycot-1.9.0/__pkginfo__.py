# pylint: disable-msg=W0622
"""cubicweb-apycot application packaging information"""

modname = 'apycot'
distname = 'cubicweb-apycot'

numversion = (1, 9, 0)
version = '.'.join(str(num) for num in numversion)

license = 'GPL'

author = 'Logilab'
author_email = 'contact@logilab.fr'

description = 'Continuous testing / integration tool for the CubicWeb framework'

web = 'http://www.cubicweb.org/project/%s' % distname

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
    ]


__depends__ = {'pyro': None,
               'cubicweb': '>= 3.6.0',
               'cubicweb-vcsfile': '>= 0.9.0',
               'cubicweb-file': None}
__recommends__ = {'cubicweb-tracker': None,
                  'cubicweb-nosylist': None}

import sys
from os import listdir as _listdir
from os.path import join, isdir

CUBES_DIR = join('share', 'cubicweb', 'cubes')
THIS_CUBE_DIR = join(CUBES_DIR, modname)

def listdir(dirpath):
    return [join(dirpath, fname) for fname in _listdir(dirpath)
            if fname[0] != '.' and not fname.endswith('.pyc')
            and not fname.endswith('~') and not isdir(join(dirpath, fname))]

from glob import glob
try:
    data_files = [
        # common files
        [THIS_CUBE_DIR,
         [fname for fname in glob('*.py') if fname != 'setup.py']],
        ]
    # check for possible extended cube layout
    for dirname in ('entities', 'views', 'sobjects', 'schema', 'data', 'i18n', 'migration',
                    'wdoc', join('wdoc', 'images')):
        if isdir(dirname):
            data_files.append([join(THIS_CUBE_DIR, dirname), listdir(dirname)])
    # Note: here, you'll need to add subdirectories if you want
    # them to be included in the debian package
except OSError:
    #print >> sys.err, we are in an installed directory
    pass
