# pylint: disable-msg=W0622
"""cubicweb-rememberme application packaging information"""

modname = 'rememberme'
distname = 'cubicweb-rememberme'

numversion = (0, 1, 2)
version = '.'.join(str(num) for num in numversion)

license = 'LCL'
copyright = '''Copyright (c) 2010 LOGILAB S.A. (Paris, FRANCE).
http://www.logilab.fr -- mailto:contact@logilab.fr'''

author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'

short_desc = 'an implementation of the Rembemer Me feature for cubicweb'
long_desc = '''an implementation of the Rembemer Me feature for cubicweb'''

web = 'http://www.cubicweb.org/project/%s' % distname


from os import listdir as _listdir
from os.path import join, isdir, exists, dirname
from glob import glob

THIS_CUBE_DIR = join('share', 'cubicweb', 'cubes', modname)

def listdir(dirpath):
    return [join(dirpath, fname) for fname in _listdir(dirpath)
            if fname[0] != '.' and not fname.endswith('.pyc')
            and not fname.endswith('~')
            and not isdir(join(dirpath, fname))]

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

__depends_cubes__ = {}
__depends__ = {'cubicweb': '>= 3.6.1'}
__use__ = ()
__recommend__ = ()

