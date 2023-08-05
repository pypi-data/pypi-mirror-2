#
# Test the EXACT commandline
#
import pyutilib.th
import unittest
import glob
import os
import os.path
import sys

currdir = os.path.dirname(os.path.abspath(__file__))+os.sep

#
# Test class
#
class Test(pyutilib.th.TestCase): pass
#
# Add test methods for each *.qa file
#
files=glob.glob(currdir+"*.qa")
for file in files:
    bname=os.path.basename(file)
    name=bname.split('.')[0]
    #cmd="cd "+currdir+"; ../../../scripts/exact -f "+name+".study.xml; find . -name \""+name+"/TEST*xml\" -exec rm -rf {} \;"
    #print cmd
    Test.add_baseline_test(cmd="cd "+currdir+"; "+sys.executable+" ../../../scripts/exact -f "+name+".study.xml; find . -name \"TEST-"+name+"*xml\" -exec rm -rf {} \;", baseline=currdir+name+".qa", name=name)
#
# Run the unittest main routine
#
if __name__ == "__main__":
   unittest.main()

