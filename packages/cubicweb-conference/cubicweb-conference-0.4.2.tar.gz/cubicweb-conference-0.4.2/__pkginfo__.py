# pylint: disable-msg=W0622
"""cubicweb-conference application packaging information"""

modname = 'conference'
distname = 'cubicweb-%s' % modname

numversion = (0, 4, 2)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'

author = 'Logilab'
author_email = 'contact@logilab.fr'

description = 'conference component for the CubicWeb framework'
short_desc = description # XXX cw < 3.8 bw compat

ftp = ''
web = 'http://www.cubicweb.org/project/%s' % distname

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
    ]

__depends_cubes__ = {'comment': None,
                     'file': None,
                     'registration': None,
                     'tag': None,
                     'forgotpwd': ">= 0.2.0",
                     }
__depends__ = {'cubicweb': '>= 3.6.1'}
for key, value in __depends_cubes__.items():
    __depends__['cubicweb-'+key] = value
__use__ = tuple(__depends_cubes__)

from os import listdir as _listdir
from os.path import join, isdir
from glob import glob

# packaging ###

CUBES_DIR = join('share', 'cubicweb', 'cubes')
THIS_CUBE_DIR = join(CUBES_DIR, 'conference')

def listdir(dirpath):
    return [join(dirpath, fname) for fname in _listdir(dirpath)
            if fname[0] != '.' and not fname.endswith('.pyc')
            and not fname.endswith('~')]

data_files = [
    # common files
    [THIS_CUBE_DIR, [fname for fname in glob('*.py') if fname != 'setup.py']],
    ]
# check for possible extended cube layout
for dirname in ('entities', 'views', 'sobjects', 'hooks', 'schema', 'data', 'i18n', 'migration', 'wdoc'):
    if isdir(dirname):
        data_files.append([join(THIS_CUBE_DIR, dirname), listdir(dirname)])
# Note: here, you'll need to add subdirectories if you want
# them to be included in the debian package
