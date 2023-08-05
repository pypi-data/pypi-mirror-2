#
# exact - process an XML file that defines an EXACT operation:
#
#        1. a computational experiment
#        2. a computational analysis
#        3. an experimental study, containing one or more experiments or
#                analyses
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
import glob
import string
from optparse import OptionParser
from os.path import abspath, dirname
import pyutilib.subprocess
from fast import exact

#
# Delete files generated during the execution of an analysis, 
# experiment, or experimental study.
#
# NOTE: this only looks for experimental study files right now...
#
def perform_cleanup():
  files = glob.glob("*.study.xml")
  for file in files:
    obj = exact.ExperimentalStudy(file,False)
    obj.clean()


#
# The 'main' function
#
def run_main(args=sys.argv):
  parser = OptionParser()
  parser.usage="exact [options...] <exp-file> [<exp-file> ...]"
  parser.description="A Python script for running an XML-defined computational experiment."
  parser.add_option("-t","--tag",
        help="Execute an experiment only if it has a matching tag element. If no tag element is specified, then run an experiment without regard to the experiment's tag element values.",
        action="append",
        dest="taglist",
        default=[])
  parser.add_option("-a","--analysis",
        help="Run an analysis.  A regular expression can be specified to run one or more analyses.",
        action="store",
        dest="analysis",
        default=None)
  parser.add_option("-e","--experiment",
        help="Run an experiment.  A regular expression can be specified to run one or more experiments.",
        action="store",
        dest="experiment",
        default=None)
  parser.add_option("-d","--debug",
        help="Add debugging information.",
        action="store_true",
        dest="debug",
        default=False)
  parser.add_option("--cleanup",
        help="Cleanup experimental files.",
        action="store_true",
        dest="cleanup",
        default=False)
  parser.add_option("-f","--force",
        help="Force the deletion of old experimental files.",
        action="store_true",
        dest="delete_old_files",
        default=False)
  (options,args) = parser.parse_args(args=sys.argv)
  if len(args) == 1:
     parser.print_help()
     sys.exit(1)
  if options.debug:
     exact.global_data.debug=True
  if options.cleanup:
     perform_cleanup()
  #
  # Get the path where this executable is located
  #
  pathname = os.path.dirname(sys.argv[0])
  fullpath = os.path.abspath(pathname)
  os.environ["PATH"] = os.environ["PATH"] + ":" + fullpath + ":" + fullpath + "/../packages/fast/scripts" + ":" +  fullpath + "/.." + ":" + fullpath + "/../../src"
  #
  # Find the virtual python installation, if it exist
  #
  rootdir=os.path.dirname(fullpath)
  while fullpath != "\\" and fullpath != "":
    if os.path.exists(rootdir+os.sep+"python"):
        os.environ["PATH"] = rootdir+os.sep+"python/bin:"+os.environ["PATH"]
        break
    rootdir=os.path.dirname(rootdir)
  #
  # Process the arguments
  #
  xmlfiles = []
  factors = []

  for arg in args[1:]:
     if exact.isint(arg):
        factors.append( eval(arg) )
     else:
        xmlfiles.append( arg )
  if options.analysis==None and options.experiment==None:
     options.analysis='.*'
     options.experiment='.*'
  else:
     options.delete_old_files=True
  load_results= (options.experiment==None)
  #
  # Process the XML files
  #
  for xmlfile in xmlfiles:
    if xmlfile == "unknown":
       print "ERROR: an experiment file has not been specified."
       sys.exit(1)
    if exact.global_data.debug and len(factors) > 0:
       print "Factors: " + factors
    #
    # Read experimental study file
    #
    # Note: this has the auto-loading of results disabled
    #
    if exact.global_data.debug==True:
       print "      Reading file: " + xmlfile
    exact_obj = exact.GenericInterface(xmlfile,load_results=load_results)
    #
    # Execute this study if it has the right tags
    #
    if isinstance(exact_obj,exact.ExperimentalStudy):
       exact_obj.execute(options.taglist,factors,force=options.delete_old_files,analysis_name=options.analysis,experiment_name=options.experiment)
    #
    # Execute this experiment
    #
    elif isinstance(exact_obj,exact.Experiment):
       exact_obj.execute(factors)
    #
    # Execute this analysis
    #
    elif isinstance(exact_obj,exact.AnalysisBase):
       exact_obj.execute()
    else:
       print "ERROR: unknown exact object type!"
       sys.exit(1)
    
def main(args=sys.argv):
    signal.signal(signal.SIGTERM, pyutilib.subprocess.signal_handler)
    signal.signal(signal.SIGINT, pyutilib.subprocess.signal_handler)
    try:
      run_main(args)
    except Exception,e:
      print "ERROR: EXACT failed to handle exception"
      raise
      if exact.global_data.debug:
         raise

