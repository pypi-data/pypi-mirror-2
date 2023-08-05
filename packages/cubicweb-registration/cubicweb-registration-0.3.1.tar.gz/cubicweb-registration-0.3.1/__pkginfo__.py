# pylint: disable-msg=W0622
"""cubicweb-registration application packaging information"""

modname = 'registration'
distname = 'cubicweb-registration'

numversion = (0, 3, 1)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
copyright = '''Copyright (c) 2009-2010 LOGILAB S.A. (Paris, FRANCE).
http://www.logilab.fr -- mailto:contact@logilab.fr'''

author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'

web = 'http://www.cubicweb.org/project/%s' % distname

short_desc = 'public registration component for the CubicWeb framework'
long_desc = """This CubicWeb component provides a public registration feature (users
can register and create an account without the need for admin
intervention).

CubicWeb is a semantic web application framework, see http://www.cubicweb.org
"""

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
    ]

__depends_cubes__ = {}
__depends__ = {'cubicweb': '>= 3.7.2',
               'python-crypto': None,
               'PIL': None,
               }
__use__ = tuple(__depends_cubes__)
__recommend__ = ()

# packaging ###

from os import listdir as _listdir
from os.path import join, isdir

pyversions = ['2.4']

CUBES_DIR = join('share', 'cubicweb', 'cubes')
THIS_CUBE_DIR = join(CUBES_DIR, 'registration')

def listdir(dirpath):
    return [join(dirpath, fname) for fname in _listdir(dirpath)
            if fname[0] != '.' and not fname.endswith('.pyc')
            and not fname.endswith('~')]

from glob import glob
try:
    data_files = [
        # common files
        [THIS_CUBE_DIR, [fname for fname in glob('*.py') if fname != 'setup.py']],
        ]
    # check for possible extended cube layout
    for dirname in ('entities', 'views', 'sobjects', 'hooks', 'schema', 'data', 'i18n', 'migration'):
        if isdir(dirname):
            data_files.append([join(THIS_CUBE_DIR, dirname), listdir(dirname)])
    # Note: here, you'll need to add subdirectories if you want
    # them to be included in the debian package
except OSError:
    # we are in an installed directory
    pass

cube_eid = None # <=== FIXME if you need direct bug-subscription
