# pylint: disable-msg=W0622
"""cubicweb-timesheet application packaging information"""

modname = 'timesheet'
distname = 'cubicweb-%s' % modname

numversion = (0, 2, 3)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
description = 'record who did what and when for the CubicWeb framework'
web = 'http://www.cubicweb.org/project/%s' % distname
author = 'Logilab'
author_email = 'contact@logilab.fr'

classifiers = [
           'Environment :: Web Environment',
           'Framework :: CubicWeb',
           'Programming Language :: Python',
           'Programming Language :: JavaScript',
           ]

__depends__ = {'cubicweb': '>= 3.6.0',
               'cubicweb-calendar':  '>= 0.1.0',
               'cubicweb-workorder': '>= 0.6.0',
               }

from os import listdir as _listdir
from os.path import join, isdir

#from cubicweb.devtools.pkginfo import get_distutils_datafiles
CUBES_DIR = join('share', 'cubicweb', 'cubes')
THIS_CUBE_DIR = join(CUBES_DIR, 'timesheet')

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
