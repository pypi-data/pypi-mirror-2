#
# runtests - recursively find tests and execute them.
#
#  _________________________________________________________________________
#
#  FAST: Python tools for software testing.
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the FAST README.txt file.
#  _________________________________________________________________________
#

import signal
import sys
import os
from optparse import OptionParser
from os.path import abspath, dirname

import pyutilib.subprocess
from pyutilib.component.core import *

#
# Declare environment for FAST's tester utility
#
PluginGlobals.push_env(PluginEnvironment("fast.testing"))

import category
import cxxtest
import exact
import tester

#
#
#
category.add_tag('granularity', 'unit', doc='Tests that validate the operation of independent software components')
category.add_tag('granularity', 'system', doc='Tests that validate the system-level operation of software')
#
# nproc - categorization based on the number of processors used in a test
#
category.add_tag('nproc', 'serial', doc='Tests that run on a single processor', default=True)
category.add_tag('nproc', 'parallel', doc='Tests that run on multiple processors')
#
# scope - categorization based on the scope of the tests
#
##category.add_tag('scope', 'coverage', doc='Tests that ensure adequate coverage of code')
category.add_tag('scope', 'smoke', doc='Tests that execute quickly and exercise basic functionality', default=True)
category.add_tag('scope', 'nightly', doc='Tests that are suitable for testing nightly builds')
category.add_tag('scope', 'performance', doc='Tests that measure code performance')
category.add_tag('scope', 'acceptance', doc='Tests used to manager releases')

# UTILIB
cxxtest.Tester(package="utilib", dir="${root}/packages/utilib/test/unit", cmd="runner")
exact.Tester(package="utilib", dir="${root}/packages/utilib/test/studies")
# COLIN
exact.Tester(package="colin", dir="${root}/packages/colin/test/studies")
cxxtest.Tester(package="colin", dir="${root}/packages/colin/test/unit")
#nose.Tester(package="colin", dir="${root}/packages/colin/test/driver")
# PEBBL
exact.Tester(package="pebbl", dir="${root}/packages/pebbl/test")
# PICO
exact.Tester(package="pico", dir="${root}/packages/pico/test")
#nose.Tester(package="pico", dir="${root}/packages/pico/test/driver")
#nose.Tester(package="pico", dir="${root}/packages/pico/test/sucasa")
# Interfaces
exact.Tester(package="interfaces", dir="${root}/packages/interfaces/test/studies")
#nose.Tester(package="interfaces", dir="${root}/packages/interfaces/test/driver")
# SCOLIB
exact.Tester(package="scolib", dir="${root}/packages/scolib/test")

PluginGlobals.pop_env()

#
# The 'main' function
#
def run_main(args=sys.argv):
  #
  # Find the virtual python installation, if it exists.    If not, the
  # root directory is assumed to be the current directory.
  #
  pathname = os.path.dirname(sys.argv[0])
  fullpath = os.path.abspath(pathname)
  rootdir=os.path.dirname(fullpath)
  while fullpath != "\\" and fullpath != "":
    if os.path.exists(rootdir+os.sep+"python"):
        os.environ["PATH"] = rootdir+os.sep+"python/bin:"+os.environ["PATH"]
        break
    rootdir=os.path.dirname(rootdir)
  #
  # Create a simple plugin application
  #
  ##app = SimpleApplication("runtests")
  #
  # Setup parser
  #
  parser = OptionParser()
  parser.usage="runtests [options...]"
  parser.description="A Python script for recursively running a diverse set of testing scripts.  Testing scripts can be configured with a plug-in framework"
  parser.add_option("-t","--tag",
        help="Execute an experiment only if it has a matching tag element. If no tag element is specified, then run an experiment without regard to the experiment's tag element values.",
        action="append",
        dest="taglist",
        default=[])
  parser.add_option("-c","--config",
        help="Specify a configuration file to load",
        action="store",
        dest="config",
        default=None)
  parser.add_option("-r","--root",
        help="Specify the root directory.",
        action="store",
        dest="root",
        default=rootdir)
  parser.add_option("--tester",
        help="Specify the type of tester that will be run.",
        action="append",
        dest="testers",
        default=[])
  parser.add_option("-v",
        help="Enable verbose output",
        action="store_true",
        dest="verbose",
        default=False)
  parser.add_option("-n",
        help="Do nothing, but print the testing operations that would have been performed",
        action="store_true",
        dest="trace",
        default=False)
  (options,args) = parser.parse_args(args=sys.argv)
  if len(args) > 1:
     parser.print_help()
     sys.exit(1)
  #
  # Define identifiers that are replaced in directory strings
  #
  identifiers={}
  identifiers["root"] = options.root
  #
  # Generate a list of tests
  #
  tests=[]
  testers = ExtensionPoint(tester.ITester, PluginGlobals.env("fast.testing"))
  if len(testers) == 0:
        PluginGlobals.pprint()
        sys.exit(-1)
  for item in testers:
        if item.match_type(options.testers) and item.match_tags(options.taglist):
            tests += item.generate(identifiers, options)
        else:
            print ". Ignoring tester %s" % item
  #
  # Apply each test
  #
  artifacts=[]
  for test in tests:
        artifacts += test.run()
  #
  # Results
  #
  print artifacts
    

def main(args=sys.argv):
    signal.signal(signal.SIGTERM, pyutilib.subprocess.signal_handler)
    signal.signal(signal.SIGINT, pyutilib.subprocess.signal_handler)
    try:
      run_main(args)
    except Exception,e:
      print "ERROR: runtests failed to handle exception"
      raise

