#  _________________________________________________________________________
#
#  FAST: Python tools for software testing.
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the FAST README.txt file.
#  _________________________________________________________________________


import re
import math
import os
import types
import sys
import commands
from exact_xml import *
from exact_globals import *
from pyutilib.misc import get_xml_text


#
# Read a DOE file
#
def read_doe(filename):
  INPUT = open(filename,"r")
  state = 0
  nfactors = 0
  ndoe = 0
  doe = []
  ctr = 0
  for line in INPUT:
    if line[0] == "#":
       continue
    elif state == 0:
       nfactors = eval(line)
       state = 1
    elif state == 1:
       ctr = ctr + 1
       if ctr == nfactors:
          state = 2
    elif state == 2:
       ndoe = eval(line)
       state = 3
       ctr = 0
    elif state == 3:
       exp = line.strip()
       ids = []
       for val in exp.split(" "):
         ids = ids + [eval(val)]
       doe = doe + [ids]
       ctr = ctr + 1
       if ctr == ndoe:
          state = 4
    else:
       print "ERROR: reached state 4 in read_doe()!"
       sys.exit(1)
  INPUT.close()
  return doe



class DesignOfExperiments(object):
    def __init__(self, node=None):
        """
        An object that contains a design of experiments
        """
        self.reset()
        if node:
           self.initialize(node)


    def reset(self):
        self.executable = ""
        self.doe_list = []
        self.prefix = "unknown"


    def initialize(self, node, prefix):
        self.reset()
        self.prefix = prefix
        self.executable = get_xml_text(node)


    def set(self, doe_list):
        self.doe_list = doe_list


    def execute(self, factors, filter):
      ffactors = factors.apply(filter)
      if len(ffactors) > 1:
         #
         # Create the DOE file if this is a nontrivial experiment
         #
         # TODO: process continuous factors
         #
         doe_input = self.prefix + ".in.doe"
         doe_output = self.prefix + ".out.doe"
         if global_data.debug:
            print "Creating DOE file:", doe_input
         OUTPUT = open(doe_input,"w")
         print >>OUTPUT, len(ffactors)
         j=0
         for factor in ffactors:
           if global_data.debug:
              print "Factor ",j,"has",len(factor),"levels"
           print >>OUTPUT, len(factor)
           j = j + 1
         OUTPUT.close()
         #
         # Launch DOE
         #
         if self.executable != "" and self.executable != "complete_doe":
            doe_log = commands.getoutput(self.executable + " " + doe_input + ">" + doe_output)
            if global_data.debug:
               print "DOE Log: \n", doe_log
         else:
            doe_log = complete_doe(doe_input,doe_output)
            if global_data.debug:
               print "DOE Log: \n", doe_log
         if not os.path.exists(doe_output):
            print "ERROR: missing file " + doe_output
            print "ERROR: the DOE code has failed to execute properly"
            sys.exit(1)
         tmp_doe_list = read_doe(doe_output)
         if not global_data.debug:
            os.unlink(doe_input)
            os.unlink(doe_output)
      else:
         #
         # Create a simple doe
         #
         tmp_doe_list = []
         for j in range(len(ffactors[0])):
           tmp_doe_list = tmp_doe_list + [ [j+1] ]
      #
      # Verify the treatments...
      #
      self.doe_list = []
      #print "DOE_LIST_LEN",len(tmp_doe_list)
      for item in tmp_doe_list:
        level_name = {}
        for i in range(0,len(factors)):
          #print "HERE",i,item[i],item
          #print "HERE",factors[i].name,factors[i].levels,len(factors[i].levels)
          if filter.treatment_value=="name":
             level_name[ str(factors[i].name) ] = str(factors[i][ item[i]-1 ].name)
          else:
             level_name[ str(factors[i].name) ] = str(factors[i][ item[i]-1 ].text)
        if filter.verify_treatment(level_name):
           #print "HERE",True
           self.doe_list.append( item )
      #print "HERE",len(self.doe_list)
      return ffactors


    def __iter__(self):
        return self.doe_list.__iter__()


    def pprint(self,prefix=""):
        print prefix + "Design of Experiments:"
        print prefix + "  Executable: " + self.executable



class DOEFactor:
     def __init__(self):
        self.nlevels=0
        self.type='s'
        self.rlower=0.0
        self.rupper=0.0


def complete_doe_recursion(OUTPUT, factors, work, i):
    for j in range(0,factors[i].nlevels):
      work[i] = j
      if (i+1) == len(factors):
         for k in range(0,len(work)):
           print >>OUTPUT, work[k]+1,
         print >>OUTPUT, ""
      else:
         complete_doe_recursion(OUTPUT,factors,work,i+1)


def comment_lines(INPUT):
        for line in INPUT:
          line = line.strip()
          if line[0] == "#":
             continue
          else:
             return line
        return None


def read_doefile(infile):
        factors = []
        INPUT = open(infile, "r")
        line = comment_lines(INPUT)
        nfactors = eval(re.split('[\t ]+',line)[0])
        for i in range(0,nfactors):
          factor = DOEFactor()
          line = comment_lines(INPUT)
          factor.nlevels = eval(re.split('[\t ]+',line)[0])
          factors.append(factor)
        return factors


def complete_doe(infile,outfile):
        factors = read_doefile(infile)
        OUTPUT = open(outfile, "w")
        #
        # Print the original DOE information
        #
        print >>OUTPUT, "#"
        print >>OUTPUT, "# Complete DOE generated from file " + outfile
        print >>OUTPUT, "#"
        print >>OUTPUT, len(factors)
        for factor in factors:
          print >>OUTPUT, factor.nlevels,
          if factor.type == 'c':
             print >>OUTPUT, "c",factor.rlower,factor.rupper
          print >>OUTPUT, ""
        #
        # Compute and print the number of designs
        #
        num=1 
        work = []
        for factor in factors:
          num = num * factor.nlevels;
          work.append(0)
        print >>OUTPUT, num
        #
        # Start the recursion
        #
        complete_doe_recursion(OUTPUT,factors,work,0)
        OUTPUT.close()


