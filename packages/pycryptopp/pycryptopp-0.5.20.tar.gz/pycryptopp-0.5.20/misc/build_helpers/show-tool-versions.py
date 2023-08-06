#! /usr/bin/env python

import os, subprocess, sys, traceback

def print_platform():
    try:
        import platform
        out = platform.platform()
        print
        print "platform:", out.replace("\n", " ")
    except EnvironmentError:
        sys.stderr.write("Got exception using 'platform'. Exception follows\n")
        traceback.print_exc(file=sys.stderr)
        pass

def print_python_ver():
    print "python:", sys.version.replace("\n", " ") + ', maxunicode: ' + str(sys.maxunicode)

def print_cmd_ver(cmdlist, label=None):
    try:
        res = subprocess.Popen(cmdlist, stdin=open(os.devnull),
                               stdout=subprocess.PIPE).communicate()[0]
        if label is None:
            label = cmdlist[0]
        print
        print label + ': ' + res.replace("\n", " ")
    except EnvironmentError:
        sys.stderr.write("Got exception invoking '%s'. Exception follows.\n" % (cmdlist[0],))
        traceback.print_exc(file=sys.stderr)
        pass

def print_as_ver():
    if os.path.exists('a.out'):
        print
        print "WARNING: a file named a.out exists, and getting the version of the 'as' assembler writes to that filename, so I'm not attempting to get the version of 'as'."
        return
    try:
        res = subprocess.Popen(['as', '-version'], stdin=open(os.devnull),
                               stderr=subprocess.PIPE).communicate()[1]
        print
        print 'as: ' + res.replace("\n", " ")
        os.remove('a.out')
    except EnvironmentError:
        sys.stderr.write("Got exception invoking '%s'. Exception follows.\n" % ('as',))
        traceback.print_exc(file=sys.stderr)
        pass

def print_setuptools_ver():
    try:
        import pkg_resources
        out = str(pkg_resources.require("setuptools"))
        print
        print "setuptools:", out.replace("\n", " ")
    except (ImportError, EnvironmentError):
        sys.stderr.write("Got exception using 'pkg_resources' to get the version of setuptools. Exception follows\n")
        traceback.print_exc(file=sys.stderr)
        pass

def print_py_pkg_ver(pkgname):
    try:
        import pkg_resources
        out = str(pkg_resources.require(pkgname))
        print
        print pkgname + ': ' + out.replace("\n", " ")
    except (ImportError, EnvironmentError):
        sys.stderr.write("Got exception using 'pkg_resources' to get the version of %s. Exception follows.\n" % (pkgname,))
        traceback.print_exc(file=sys.stderr)
        pass
    except pkg_resources.DistributionNotFound:
        sys.stderr.write("pkg_resources reported no %s package installed. Exception follows.\n" % (pkgname,))
        traceback.print_exc(file=sys.stderr)
        pass

print_platform()

print_python_ver()

print_cmd_ver(['buildbot', '--version'])
print_cmd_ver(['cl'])
print_cmd_ver(['g++', '--version'])
print_cmd_ver(['cryptest', 'V'])
print_cmd_ver(['darcs', '--version'])
print_cmd_ver(['darcs', '--exact-version'], label='darcs-exact-version')
print_cmd_ver(['7za'])

print_as_ver()

print_setuptools_ver()

print_py_pkg_ver('coverage')
print_py_pkg_ver('trialcoverage')
print_py_pkg_ver('setuptools_trial')
print_py_pkg_ver('setuptools_darcs')
print_py_pkg_ver('darcsver')
