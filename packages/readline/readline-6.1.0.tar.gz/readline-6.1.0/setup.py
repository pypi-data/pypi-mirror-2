#!/usr/bin/env python

import os
import os.path
import sys
import distutils

from setuptools import setup, Extension


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.rst')).read()

VERSION = '6.1.0'
DESCRIPTION = 'The standard Python readline extension statically linked against the GNU readline library.'
LONG_DESCRIPTION = README + '\n\n' + NEWS
CLASSIFIERS = [
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX',
    'Programming Language :: C',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

# If we are on Mac OS 10.5 or later, attempt a universal binary, which is the way
# the original system version of readline.so was compiled. Set up flags here.
if distutils.util.get_platform().find('macosx-10.5') == 0:
    UNIVERSAL = '-isysroot /Developer/SDKs/MacOSX10.5.sdk ' + \
                '-arch i386 -arch ppc -arch x86_64 -arch ppc64'
elif distutils.util.get_platform().find('macosx-10.6') == 0:
    # Snow Leopard only has 3 architectures
    UNIVERSAL = '-isysroot /Developer/SDKs/MacOSX10.6.sdk ' + \
                '-arch i386 -arch ppc -arch x86_64'
else:
    UNIVERSAL = ''

# Since we have the latest readline (post 4.2), enable all readline functionality
# These macros can be found in pyconfig.h.in in the main directory of the Python tarball
DEFINE_MACROS = [
    ('HAVE_RL_CALLBACK', None),
    ('HAVE_RL_CATCH_SIGNAL', None),
    ('HAVE_RL_COMPLETION_APPEND_CHARACTER', None),
    ('HAVE_RL_COMPLETION_DISPLAY_MATCHES_HOOK', None),
    ('HAVE_RL_COMPLETION_MATCHES', None),
    ('HAVE_RL_COMPLETION_SUPPRESS_APPEND', None),
    ('HAVE_RL_PRE_INPUT_HOOK', None),
]

# Check if any of the distutils commands involves building the module,
# and check for quiet vs. verbose option
building = False
verbose = True
for s in sys.argv[1:]:
    if s.startswith('bdist') or s.startswith('build') or s.startswith('install'):
        building = True
    if s in ['--quiet', '-q']:
        verbose = False
    if s in ['--verbose', '-v']:
        verbose = True
    
# Build readline first, if it is not there and we are building the module
if building and not os.path.exists('readline/libreadline.a'):
    if verbose:
        print("\n============ Building the readline library ============\n")
        os.system('cd rl && /bin/bash ./build.sh')
        print("\n============ Building the readline extension module ============\n")
    else:
        os.system('cd rl && /bin/bash ./build.sh > /dev/null 2>&1')        
    # Add symlink that simplifies include and link paths to real library
    if not (os.path.exists('readline') or os.path.islink('readline')):
        os.symlink(os.path.join('rl','readline-lib'), 'readline')

setup(
    name="readline",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    maintainer="Ludwig Schwardt; Sridhar Ratnakumar",
    maintainer_email="ludwig.schwardt@gmail.com; readline@srid.name",
    url="http://github.com/ludwigschwardt/python-readline",
    license="GNU GPL",
    platforms=['MacOS X', 'Posix'],
    include_package_data=True,
    ext_modules=[
        Extension(name="readline",
                  sources=["Modules/%s.x/readline.c" % (sys.version_info[0],)],
                  include_dirs=['.'],
                  define_macros=DEFINE_MACROS,
                  extra_compile_args=['-Wno-strict-prototypes'] + UNIVERSAL.split(),
                  extra_link_args=UNIVERSAL.split(),
                  extra_objects=['readline/libreadline.a', 'readline/libhistory.a'], 
                  libraries=['ncurses']
        ),
    ],
    zip_safe=False,
)
