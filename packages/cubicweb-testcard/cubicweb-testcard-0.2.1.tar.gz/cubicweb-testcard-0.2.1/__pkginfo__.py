# pylint: disable-msg=W0622
"""cubicweb-testcard application packaging information"""

modname = 'testcard'
distname = 'cubicweb-testcard'

numversion = (0, 2, 1)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'

author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'

description = 'test card component for the cubicweb framework'
short_desc = description # cw < 3.8 bw compat

web = 'http://www.cubicweb.org/project/%s' % distname

__depends_cubes__ = {'card': None,
                     'tracker': '>= 1.1.0'}
__depends__ = {'cubicweb': '>= 3.6.0'}
for key,value in __depends_cubes__.items():
    __depends__['cubicweb-'+key] = value

__recommends_cubes__ = {'comment': None}
__recommends__ = {'cubicweb-comment': None}

# XXX cw < 3.8 bw compat
__use__ = tuple(__depends_cubes__)
__recommend__ = tuple(__recommends_cubes__)


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
