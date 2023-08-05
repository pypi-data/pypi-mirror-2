# pylint: disable-msg=W0622
"""cubicweb-blog packaging information"""

modname = 'blog'
distname = "cubicweb-%s" % modname

numversion = (1, 7, 4)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'

author = "Logilab"
author_email = "contact@logilab.fr"
web = 'http://www.cubicweb.org/project/%s' % distname

description = "blogging component for the CubicWeb framework"
short_desc = description # XXX cw < 3.8 bw compat

classifiers = [
    'Environment :: Web Environment'
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
    ]

__depends__ = {'cubicweb': '>= 3.7.3'}
__recommends_cubes__ = {'tag': None,
                        'comment': '>= 1.6.3'}
__recommends__ = {}
for cube in __recommends_cubes__:
    __recommends__['cubicweb-'+cube] = __recommends_cubes__[cube]


# package ###

from os import listdir as _listdir
from os.path import join, isdir, exists
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
for dname in ('entities', 'views', 'sobjects', 'hooks', 'schema', 'data', 'i18n', 'migration'):
    if isdir(dname):
        data_files.append([join(THIS_CUBE_DIR, dname), listdir(dname)])
