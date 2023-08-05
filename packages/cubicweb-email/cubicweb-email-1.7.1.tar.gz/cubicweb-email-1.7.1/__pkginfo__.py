# pylint: disable-msg=W0622
"""cubicweb-email packaging information"""

modname = 'email'
distname = "cubicweb-%s" % modname

numversion = (1, 7, 1)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'

author = "Logilab"
author_email = "contact@logilab.fr"
web = 'http://www.cubicweb.org/project/%s' % distname

short_desc = "email component for the CubicWeb framework"
long_desc = """\
This cube models multipart email messages (`Emails` and `EmailPart`) and
provides tools to import your mail box into a cubicweb instance.

Email are automatically stored into`EmailThreads`.
"""

# used packages
__depends__ = {'cubicweb': '>= 3.6.0',
               'cubicweb-file': '>= 1.6.0'}
__recommends__ = {'cubicweb-comment': None}

# XXX cw < 3.8 bw compat
__use__ = ('file',)
__recommend__ = ('comment',)

classifiers = [
           'Environment :: Web Environment',
           'Framework :: CubicWeb',
           'Programming Language :: Python',
           'Programming Language :: JavaScript',
]


from os import listdir as _listdir
from os.path import join, isdir
from glob import glob

def listdir(dirpath):
    return [join(dirpath, fname) for fname in _listdir(dirpath)
            if fname[0] != '.' and not fname.endswith('.pyc')
            and not fname.endswith('~')]

CUBES_DIR = join('share', 'cubicweb', 'cubes')
THIS_CUBE_DIR = join(CUBES_DIR, modname)

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

