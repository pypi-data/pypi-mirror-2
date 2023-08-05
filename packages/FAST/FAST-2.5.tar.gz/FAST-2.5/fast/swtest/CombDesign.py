#  _________________________________________________________________________
#
#  FAST: Python tools for software testing.
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the FAST README.txt file.
#  _________________________________________________________________________

"""
This file implements the IPOG functor, which generates a combinatorial
design that is appropriate for software testing.

This implementation of IPOG is adapted from the description in 

  Y. Lei, R. Kacker, D. R. Kuhn, V. Okun and J. Lawrence,
  IPOG/IPOG-D: efficient test generation for multi-way combinatorial testing,
  SOFTWARE TESTING, VERIFICATION AND RELIABILITY, 2007, Wiley Interscience, 
  (www.interscience.wiley.com).


William E. Hart
March 10, 2008
"""

import sys
sys.path = sys.path + ["../.."]

import copy
import operator
from pyutilib.misc import cross_iter, Bunch
from pyutilib.math import perm, factorial

class CombDesign(object):
    """
    A class for storing a combinatorial design.
    """

    def __init__(self):
        """
        Create the CombDesign object
        """
        self.clear()

    def clear(self):
        """
        Clear the data from a design object
        """
        self.ncol = 0
        self._col = []
        self._parameter = []
        self.design = []
        self._relation = {}
        self._constraints = {}

    def reset(self):
        """
        Reset a design object to get ready to develop a new design.
        """
        self.setup()
        self.design = None

    def num(self):
        """
        Returns a list of 
        """
        return map(lambda x: x.num, self._col)

    def add_row(self,row):
        if self.design is None:
           self.design = []
        if len(row) < len(self._col):
           self.design = self.design + [list(row) + [-1]*(len(self._col)-len(row))]
        else:
           self.design = self.design + [list(row)]

    def add(self,parameter,levels):
        """
        Add a parameter and its associated levels
        """
        if parameter in self._parameter:
           raise KeyError, "Parameter name "+parameter+" already exists."
        if not type(levels) is list:
           raise ValueError, "Parameter "+parameter+\
                    " must be setup with a list of parameter levels."
        if None in levels:
           raise ValueError, "None is not a valid value in the levels of parameter "+parameter
        if len(levels) < 2:
           raise ValueError, "Parameeter "+parameter+\
                    " must have 2 or more levels"
        self._col.append( 
                    Bunch(name=parameter, num=len(levels), levels=levels) )
        self._parameter.append( self._col[-1] )

    def define_relation(self, relation, parameter, levels):
        if relation not in self._relation:
           self._relation[relation] = {}
        self._relation[relation][parameter] = levels

    def define_constraint(self, relation):
        pass

    def valid_combinations(self,t=2,mask=None):
        #
        # The default mask is the first t columns
        #
        if mask is None:
           mask=range(0,t)
        else:
           tmp=[]
           for i in range(0,len(mask)):
             if mask[i] == 1:
                tmp.append(i)
           mask=tmp
        #
        # If there are no relations, then consider all valid
        # combinations.
        #
        if len(self._relation) == 0:
           sets = {}
           for i in mask:
             sets[i] = self._col[i].levels
           for x in self._valid_combinations(sets):
             yield x
        #
        # Otherwise, use the relations to generate valid combinations
        #
        else:
           for key in self._relation:
             sets = {}
             for i in mask:
               sets[i] = self._relation[key][self._col.name]
             for x in self._valid_combinations(sets,name):
               yield x

    def _valid_combinations(self,sets,relation=None):
        """
        Generates combinations of the levels specified for different
        parameters.  If 'relation' is not None, then these combinations
        are validated with the relation constraint values.
        """
        keys=sets.keys()
        keys.sort(reverse=True)
        wheels={}
        for key in keys:
          wheels[key] = iter(sets[key])      # wheels like in an odometer
        digits = {}
        for key in wheels:
          digits[key] = wheels[key].next()
        while True:
            flag=True
            if relation is not None:
               for constraint in self._constraints[relation]:
                 pass
            if flag:
               yield copy.copy(digits)
            for key in keys:
                try:
                    digits[key] = wheels[key].next()
                    break
                except StopIteration:
                    wheels[key] = iter(sets[key])
                    digits[key] = wheels[key].next()
            else:
                break

    def print_design(self):
        if self.design is None:
           return
        for row in self.design:
          for i in row:
            print str(i)+" ",
          print ""

    def setup(self):
        self._col.sort(key=lambda x:x.num,reverse=True)
        self.ncol = len(self._col)
        
    def __iter__(self):
        return self.design.__iter__()

    def __str__(self):
        ans = ""
        self.setup()
        first=True
        for key in self._parameter:
          if not first:
             ans = ans + "\n"
          first=False
          ans = ans + key.name + ":"
          for item in key.levels:
            ans = ans + " "+str(item)
        return ans

    def match(self,row,mask,t):
        for i in mask:
          try:
             if row[i] is not None and row[i] != mask[i]:
                return False
          except IndexError, err:
             print "ERROR",row,mask
        return True

    def validate(self,t):
        for i in range(t,self.ncol+1):
          if t == i:
             for x in self.valid_combinations(t):
               flag=False
               for row in self.design:
                 if self.match(row,x,t):
                    flag=True
                    break
               if not flag:
                  raise ValueError, "Invalid design: mask="+str(x)
          else:
             for x in self._masked_valid_combinations(t, i):
               flag=False
               for row in self.design:
                 if self.match(row,x,t):
                    flag=True
                    break
               if not flag:
                  raise ValueError, "Invalid design: mask="+str(x)

    def _masked_valid_combinations(self, t, i):
        """
        This function iterates over each mask, which is a vector of 1s and 0s.
        Each mask reflects a t-interaction that needs to be covered.  For
        a given value of 'i', the mask has a 1 at position i-1, and zeros
        afterward.  Thus, this function iterates over the t-1 1s in 
        positions 0..i-2.

        For each mask generated, the CombDesign.valid_combinations
        method is called to generate all masked lists of values that 
        need to be covered by a design.

        TODO: rework this to manage a list of integer representing the
        ones.
        """
        #print "HERE",t,i
        if i == t:
           #print "MASK A:"
           yield [ [1]*self.ncol ]
           return
        tmp = [0]*self.ncol
        for j in range(0,t-1):
          tmp[j] = 1
        #print self.ncol,i
        tmp[i-1] = 1
        for x in self.valid_combinations(t,mask=tmp):
          #print "MASK B:",tmp
          yield x
        g = t-1
        while True:
          if tmp[0] == 1:
             tmp[g] = 1
             g=g-1
             tmp[g] = 0
             for x in self.valid_combinations(t,mask=tmp):
               #print "MASK C:",tmp,g
               yield x
          else:
             g=g+1
             while g<i and (tmp[g] == 0):
               g=g+1
             if g==i:
                break
             n=0
             while g<i and (tmp[g] == 1):
               n=n+1
               g=g+1
             if g==i:
                break
             tmp[g]=1
             while g>=n:
               g=g-1
               tmp[g]=0
             for j in range(0,g):
               tmp[j]=1
             for x in self.valid_combinations(t,mask=tmp):
               #print "MASK D:",tmp,g
               yield x
 



class IPOG_solver(object):

    def __init__(self):
        """
        Constructor
        """
        self.num = None
        self.ncol = 0


    def valid_combinations(self, t, design, i):
        if t == i:
           for x in design.valid_combinations(t):
             yield x
        else:
           for x in design._masked_valid_combinations(t, i):
             yield x

    def merge(self,row,mask,t):
        for i in mask:
          if row[i] is None:
             row[i] = mask[i]

    def __call__(self, t, design,output='quiet'):
        design.reset()
        self.num = design.num()
        self.ncol = len(self.num)
        #
        # Add a test for each combination of values of the first t parameters
        #
        if output=="normal" or output=="debugging":
           print "Creating initial design...",
        args = []
        for i in range(0,t):
          args = args + [range(0,self.num[i])]
        for val in self.valid_combinations(t,design,t):
          row=[None]*self.ncol
          self.merge(row,val,t)
          design.add_row(row)
        if output=="normal" or output=="debugging":
           print "done."
        if output=="debugging":
           design.print_design()
        #
        # Iterative extend the rows and columns of this design
        #
        for i in range(t+1,self.ncol+1):
          #
          # Get interaction masks
          #
          pi = {}
          for x in self.valid_combinations(t, design, i):
            if x[i-1] not in pi:
               pi[x[i-1]] = []
            pi[x[i-1]].append(x)
          #
          # Extend the column
          #
          if output=="normal" or output=="debugging":
             print "Extending the design..."
          for row in design:
            #print "HERE",pi.keys()
            if output=="debugging":
               print "ROW",row
            #
            # Find the level that removes the most interactions from 
            # the set of all interactions
            #
            best_num=-1
            best_level=None
            for level in pi:
              if level is None:
                 raise ValueError, "Unexpected 'None' level: "+str(pi.keys())
              num=0
              #row[i-1]=level
              for mask in pi[level]:
                if output=="debugging":
                   print row,mask,design.match(row,mask,t)
                if design.match(row,mask,t):
                   num=num+1
              if output=="debugging":
                 print i,row,level,num
              #
              # TODO: reconsider whether ties should be broken in a more
              # 'random' manner.
              #
              if num>=best_num:
                 best_num=num
                 best_level=copy.copy(level)
            if best_level is None:
               raise ValueError, "ERROR: did not find a best level"
            #
            # Set this level in this row, and remove the matched interactions
            #
            row[i-1] = best_level
            tmp=[]
            for mask in pi[best_level]:
              if not design.match(row,mask,t):
                 tmp.append(mask)
            pi[best_level]=tmp
            #print "THERE",pi.keys()
          #
          # Print
          #
          if output=="debugging":
             print ""
             print "Extended Design Column",i
             design.print_design()
             num=0
             for level in pi:
               num=num+len(pi[level])
             print "Num Interactions Remaining:",num
          #
          # Add rows
          #
          tmprows = []
          for level in pi:
            for mask in pi[level]:
              nomatch=True
              for row in tmprows:
                if design.match(row,mask,t):
                   self.merge(row,mask,t)
                   nomatch=False
                   break
              if nomatch:
                 tmp=[None]*self.ncol
                 self.merge(tmp,mask,t)
                 tmprows.append(tmp)
          for row in tmprows:
            design.add_row(row)
          #print "THERE",pi.keys()
          #
          # Print
          #
          if output=="debugging":
             print ""
             print "Extended Design Rows",i
             design.print_design()
          #print "THERE",pi.keys()
        #
        # Is there a smarter way to do this final initialization of
        # the DONT-CARE values?
        #
        for row in design:
          if None in row:
             for i in range(0,self.ncol):
               if row[i] is None:
                  row[i] = design._col[i].levels[0]
        #
        # Return design
        #
        return design

IPOG = IPOG_solver()
    

# This doesn't work anymore
def _test():
   for i in range(1,8):
     for j in range(1,i+1):
       tmp=[]
       tmp = IPOG._create_masks(j,i)
       for val in tmp:
         if sum(val) != j:
            print "ERROR: ",j,i,val
       if len(tmp) != perm(i,j):
          print "ERROR: ",j,i,perm(i,j)

import time

def print_timing(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print '%s took %0.3f s' % (func.func_name, (t2-t1))
        return res
    return wrapper

@print_timing
def _test2(t,cd):
   #return IPOG(t,cd)
   return IPOG(t,cd,"debugging")


if __name__ == '__main__':
   cd = CombDesign()
   cd.add("A",[1,2])
   cd.add("C",['a','b','c'])
   cd.add("B",[100,200,300,400])
   cd.add("D",[0,1])
   cd.add("E",[0,1])
   print cd

   IPOG(2,cd)
   print "FINAL"
   cd.print_design()
   cd.validate(2)

   IPOG(3,cd,output="quiet")
   print "FINAL"
   cd.print_design()
   cd.validate(3)

   cd = CombDesign()
   #for jj in range(3,15):
   for jj in range(9,10):
     for ii in range(0,jj):
       cd.add(str(ii),[1,2,3,4])
     cd = _test2(3,cd)
     print jj,"Size:",len(cd.design)
     cd.validate(3)


