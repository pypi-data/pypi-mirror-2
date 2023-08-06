#!/usr/bin/env python

# pycryptopp -- Python wrappers for Crypto++
#
# Copyright (C) 2009-2010 Zooko Wilcox-O'Hearn
# Author: Zooko Wilcox-O'Hearn
# See README.txt for licensing information.

import os, platform, re, subprocess, sys

from setuptools import Extension, find_packages, setup

# ECDSA isn't yet supported, but it can be turned on by testing purposes.  But
# you'll have to comment-in some lines in the C++ code to make it work.  Also
# comment-in the unit tests.
ECDSA=False
# ECDSA=True

DEBUG=False
if "--debug" in sys.argv:
    DEBUG=True
    sys.argv.remove("--debug")

DISABLE_EMBEDDED_CRYPTOPP=False
if "--disable-embedded-cryptopp" in sys.argv:
    DISABLE_EMBEDDED_CRYPTOPP=True
    sys.argv.remove("--disable-embedded-cryptopp")

# Unfortunately stdeb v0.3 doesn't seem to offer a way to pass command-line
# arguments to setup.py when building for Debian, but it does offer a way to
# pass environment variables, so we here check for that in addition to the
# command-line argument check above.
if os.environ.get('PYCRYPTOPP_DISABLE_EMBEDDED_CRYPTOPP') == "1":
    DISABLE_EMBEDDED_CRYPTOPP=True

TEST_DOUBLE_LOAD=False
if "--test-double-load" in sys.argv:
    TEST_DOUBLE_LOAD=True
    sys.argv.remove("--test-double-load")

# There are two ways that this setup.py script can build pycryptopp, either by using the
# Crypto++ source code bundled in the pycryptopp source tree, or by linking to a copy of the
# Crypto++ library that is already installed on the system.

extra_compile_args=[]
extra_link_args=[]
define_macros=[]
undef_macros=[]
libraries=[]
ext_modules=[]
include_dirs=[]
library_dirs=[]
extra_srcs=[] # This is for Crypto++ .cpp files if they are needed.

#
# Fix the build on OpenBSD
# http://allmydata.org/trac/pycryptopp/ticket/32
#
if 'openbsd' in platform.system().lower():
    extra_link_args.append("-fpic")

if DEBUG:
    extra_compile_args.append("-O0")
    extra_compile_args.append("-g")
    extra_compile_args.append("-Wall")
    extra_link_args.append("-g")
    undef_macros.append('NDEBUG')
else:
    extra_compile_args.append("-w")

if DISABLE_EMBEDDED_CRYPTOPP:
    # Link with a Crypto++ library that is already installed on the system.

    for inclpath in ["/usr/local/include/cryptopp", "/usr/include/cryptopp"]:
        if os.path.exists(inclpath):
            libraries.append("cryptopp")
            incldir = os.path.dirname(inclpath)
            include_dirs.append(incldir)
            libdir = os.path.join(os.path.dirname(incldir), "lib")
            library_dirs.append(libdir)
            break

    if not libraries:
        print "Did not locate libcryptopp in the usual places."
        print "Adding /usr/local/{include,lib} and -lcryptopp in the hopes"
        print "that they will work."

        # Note that when using cygwin build tools (including gcc) to build
        # Windows-native binaries, the os.path.exists() will not see the
        # /usr/local/include/cryptopp directory but the subsequent call to g++
        # will.
        libraries.append("cryptopp")
        include_dirs.append("/usr/local/include")
        library_dirs.append("/usr/local/lib")

else:
    # Build the Crypto++ library which is included by source code in the pycryptopp tree and
    # link against it.
    include_dirs.append(".")

    if 'sunos' in platform.system().lower():
        extra_compile_args.append('-Wa,--divide') # allow use of "/" operator

    if 'win32' in sys.platform.lower():
        try:
            res = subprocess.Popen(['cl'], stdin=open(os.devnull), stdout=subprocess.PIPE).communicate()
        except EnvironmentError, le:
            # Okay I guess we're not using the "cl.exe" compiler.
            using_msvc = False
        else:
            using_msvc = True
    else:
        using_msvc = False

    if using_msvc:
        # We can handle out-of-line assembly.
        cryptopp_src = [ os.path.join('cryptopp', x) for x in os.listdir('cryptopp') if x.endswith(('.cpp', '.asm')) ]
    else:
        # We can't handle out-of-line assembly.
        cryptopp_src = [ os.path.join('cryptopp', x) for x in os.listdir('cryptopp') if x.endswith('.cpp') ]

    # Something -- I know now what -- is creating files named
    # "._$FNAME", for example "._rdtables.cpp", and those files
    # contain uncompilable data that is not C++, thus on occasion
    # causing the build to fail. This works-around that:
    cryptopp_src = [ c for c in cryptopp_src if not c.startswith('._') ]

    extra_srcs.extend(cryptopp_src)

# In either case, we must provide a value for CRYPTOPP_DISABLE_ASM that
# matches the one used when Crypto++ was originally compiled. The Crypto++
# GNUmakefile tests the assembler version and only enables assembly for
# recent versions of the GNU assembler (2.10 or later). The /usr/bin/as on
# Mac OS-X 10.6 is too old.

try:
    sp = subprocess.Popen(['as', '-v'], stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          universal_newlines=True)
    sp.stdin.close()
    sp.wait()
    if re.search("GNU assembler version (0|1|2.0)", sp.stderr.read()):
        define_macros.append(('CRYPTOPP_DISABLE_ASM', 1))
except EnvironmentError:
    # Okay, nevermind. Maybe there isn't even an 'as' executable on this
    # platform.
    pass
else:
    try:
        # that "as -v" step creates an empty a.out, so clean it up. Modern GNU
        # "as" has --version, which emits the version number without actually
        # assembling anything, but older versions only have -v, which emits a
        # version number and *then* assembles from stdin.
        os.unlink("a.out")
    except EnvironmentError:
        pass

trove_classifiers=[
    "Environment :: Console",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "License :: DFSG approved",
    "License :: Other/Proprietary License",
    "Intended Audience :: Developers",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: Unix",
    "Operating System :: MacOS :: MacOS X",
    "Natural Language :: English",
    "Programming Language :: C",
    "Programming Language :: C++",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.4",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Topic :: Software Development :: Libraries",
    ]

PKG='pycryptopp'
VERSIONFILE = os.path.join(PKG, "_version.py")
verstr = "unknown"
try:
    verstrline = open(VERSIONFILE, "rt").read()
except EnvironmentError:
    pass # Okay, there is no version file.
else:
    VSRE = r"^verstr = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        verstr = mo.group(1)
    else:
        print "unable to find version in %s" % (VERSIONFILE,)
        raise RuntimeError("if %s.py exists, it is required to be well-formed" % (VERSIONFILE,))

srcs = ['pycryptopp/_pycryptoppmodule.cpp', 'pycryptopp/publickey/rsamodule.cpp', 'pycryptopp/hash/sha256module.cpp', 'pycryptopp/cipher/aesmodule.cpp']
if ECDSA:
    srcs.append('pycryptopp/publickey/ecdsamodule.cpp')
if TEST_DOUBLE_LOAD:
    srcs.append('_testdoubleloadmodule.cpp', )

ext_modules.append(
    Extension('pycryptopp._pycryptopp', extra_srcs + srcs, include_dirs=include_dirs, library_dirs=library_dirs, libraries=libraries, extra_link_args=extra_link_args, extra_compile_args=extra_compile_args, define_macros=define_macros, undef_macros=undef_macros)
    )

if TEST_DOUBLE_LOAD:
    ext_modules.append(
        Extension('_testdoubleload', extra_srcs + srcs, include_dirs=include_dirs, library_dirs=library_dirs, libraries=libraries, extra_link_args=extra_link_args, extra_compile_args=extra_compile_args, define_macros=define_macros, undef_macros=undef_macros)
        )

miscdeps=os.path.join(os.getcwd(), 'misc', 'dependencies')
dependency_links=[os.path.join(miscdeps, t) for t in os.listdir(miscdeps) if t.endswith(".tar")]
setup_requires = []
install_requires = ['setuptools >= 0.6a9'] # for pkg_resources for loading test vectors for unit tests

# The darcsver command from the darcsver plugin is needed to initialize the
# distribution's .version attribute. (It does this either by examining darcs
# history, or if that fails by reading the pycryptopp/_version.py
# file). darcsver will also write a new version stamp in
# pycryptopp/_version.py, with a version number derived from darcs
# history. Note that the setup.cfg file has an "[aliases]" section which
# enumerates commands that you might run and specifies that it will run
# darcsver before each one. If you add different commands (or if I forgot some
# that are already in use), you may need to add it to setup.cfg and configure
# it to run darcsver before your command, if you want the version number to be
# correct when that command runs.  http://pypi.python.org/pypi/darcsver
setup_requires.append('darcsver >= 1.2.0')

# setuptools_pyflakes is needed only if you want "./setup.py flakes" to run
# pyflakes on all the pycryptopp modules.
if 'flakes' in sys.argv[1:]:
    setup_requires.append('setuptools_pyflakes >= 1.0.0')

# setuptools_darcs is required to produce complete distributions (such as
# with "sdist" or "bdist_egg"), unless there is a
# pycryptopp.egg-info/SOURCES.txt file present which contains a complete list
# of needed files.
# http://pypi.python.org/pypi/setuptools_darcs
setup_requires.append('setuptools_darcs >= 1.0.5')

# stdeb is required to produce Debian files with "sdist_dsc".
# http://github.com/astraw/stdeb/tree/master
if "sdist_dsc" in sys.argv:
    setup_requires.append('stdeb')

data_fnames=['COPYING.GPL', 'COPYING.TGPPL.html', 'README.txt']

# In case we are building for a .deb with stdeb's sdist_dsc command, we put the
# docs in "share/doc/pycryptopp".
doc_loc = "share/doc/" + PKG
data_files = [(doc_loc, data_fnames)]

if ECDSA:
    long_description='RSA-PSS-SHA256 signatures, ECDSA(1363)/EMSA1(SHA-256) signatures, SHA-256 hashes, and AES-CTR encryption'
else:
    long_description='RSA-PSS-SHA256 signatures, SHA-256 hashes, and AES-CTR encryption'

def _setup(test_suite):
    setup(name=PKG,
          version=verstr,
          description='Python wrappers for the Crypto++ library',
          long_description=long_description,
          author='Zooko O\'Whielacronx',
          author_email='zooko@zooko.com',
          url='http://allmydata.org/trac/' + PKG,
          license='GNU GPL',
          packages=find_packages(),
          include_package_data=True,
          exclude_package_data={
              '': [ '*.cpp', '*.hpp', ]
              },
          data_files=data_files,
          setup_requires=setup_requires,
          install_requires=install_requires,
          dependency_links=dependency_links,
          classifiers=trove_classifiers,
          ext_modules=ext_modules,
          test_suite=test_suite,
          zip_safe=False, # I prefer unzipped for easier access.
          )

test_suite_name=PKG+".test"
try:
    _setup(test_suite=test_suite_name)
except Exception, le:
    # to work around a bug in Elisa v0.3.5
    # https://bugs.launchpad.net/elisa/+bug/263697
    if "test_suite must be a list" in str(le):
        _setup(test_suite=[test_suite_name])
    else:
        raise
