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
import string
import random
import time

from doe import *
from exact_xml import *
import pyutilib.subprocess
from pyutilib.misc import get_xml_text, Bunch, quote_split, escape, recursive_delete, add_method
from pyutilib.math import isint

if sys.platform == "win32":
   from time import clock
else:
   from time import time as clock

class OptionValueDictionary:
    def __init__(self):
        self.my_dict = {}

    def __getitem__(self, option):
        if option in self.my_dict.keys():
                if len(self.my_dict[option]) == 1:
                        return self.my_dict[option][0]
                else:
                        return self.my_dict[option]
        else:
                return None

    def value(self, option, index=0):
        if option in self.my_dict.keys():
                return self.my_dict[option][index]
        else:
                return None

    def __setitem__(self, option, value):
        if option in self.my_dict.keys():
                self.my_dict[option].append(value)
        else: 
                self.my_dict[option] = [ value ]

    def set(self, option, value):
        self.my_dict[option] = [ value ]

    def size(self, option):
        if option in self.my_dict.keys():
                return len(self.my_dict[option])
        else:
                return 0

    def keys(self):
        return self.my_dict.keys()

    def __iter__(self):
        """
        Returns the iterator to the keys of the dictionary.  This method allows
        a TreatmentCombinations() object to be treated as the generator for the 
        iterator of the list of ExperimentalTrial().
        """
        return self.my_dict.keys().__iter__()



def process_input_file(filename,hybrid=False):
  INPUT = open(filename,"r")
  factor_name = {}
  factor = {}
  option = OptionValueDictionary()
  state = 0
  for line in INPUT:
    #
    # Gathering up text from a multi-line factor value
    #
    if state == 1:
       if line.strip() == "\"\"\"":
          factor[tmp_factor_name] = tmp_factor_text
          state = 0
       else:
          tmp_factor_text = tmp_factor_text + line
       continue

    #
    # Get everything after the first whitespace
    #
    tmp = re.split('([\t ]+)',line.strip(),maxsplit=1)
    if len(tmp) == 1:
       if tmp[0] != "":
          words = [tmp[0], "" ]
    else:
       words = [tmp[0], tmp[2] ]
    #
    # For each option/value pair, set the option value
    #
    if len(words[1]) >=1 and words[1][0] == '$':
       try:
         option[words[0]] = eval(os.environ[words[1][1:]])
       except:
         option[words[0]] = os.environ[words[1][1:]]
    else:
       try:
         option[words[0]] = eval(words[1])
       except:
         option[words[0]] = words[1]
    #
    # For each factor, process the value
    #
    if words[0][:8] == "_factor_":
       tokens = words[0].split("_")
       if tokens[3] == "value":
          if words[1] == "\"\"\"":
             #
             # Start processing a multi-line factor value
             #
             state=1
             tmp_factor_text=""
             tmp_factor_name=factor_name[tokens[2]]
          else:
             try:
               factor[factor_name[tokens[2]]] = eval(words[1])
             except:
               factor[factor_name[tokens[2]]] = words[1]
          #try:
          #  option[factor_name[tokens[2]]] = eval(factor[factor_name[tokens[2]]])
          #except:
          #  option[factor_name[tokens[2]]] = factor[factor_name[tokens[2]]]
       elif tokens[3] == "name":
          factor_name[tokens[2]] = words[1]
  INPUT.close()
  if hybrid==False:
     return (factor,option)
  #
  # Process options to generate per-solver options.  This is needed to
  # support parameterization of hybrid solvers.
  #
  solvers = []
  solver_options = {}
  if "solver" in option.keys():
     solvers = option["solver"].split("-")
     if len(solvers) == 1:
        #print "HERE",option
        solver_options[solvers[0]] = option
     else:
        fdone = {}
        #print "HERE",factor.keys()
        for fname in factor.keys():
          fdone[fname] = False
        for solver in solvers:
          solver_options[solver] = {}
          for fname in factor.keys():
            #print "HERE",fname, solver
            if not fdone[fname] and fname[0:(len(solver)+1)] == solver + "_":
               fdone[fname] = True
               tmp = re.split('([\t ]+)',factor[fname])
               for item in tmp:
                 tokens = item.split("=")
                 if len(tokens) == 2:
                    solver_options[solver][tokens[0]] = tokens[1]
                 else:
                    solver_options[solver][item] = "ExactNone"
        #
        # options not assigned to any solver are assigned to the
        # master solver
        #
        for fname in factor.keys():
          if not fdone[fname]:
             tmp = re.split('([\t ]+)',factor[fname])
             for item in tmp:
               tokens = item.split("=")
               if len(tokens) == 2:
                  solver_options[solvers[0]][tokens[0]] = tokens[1]
               else:
                  solver_options[solvers[0]][item] = "ExactNone"
     #
     # Replace option value if it starts with a '_'
     #
     for solver in solvers:
       tmp = []
       for opt in solver_options[solver]:
         val = solver_options[solver][opt]
         #print "SOLVER: ",solver," OPTION: ",opt," VALUE: ",val
         if opt[0] != "_" and isinstance(val,types.StringType) and val is not None and val[0] == "_":
            if val in option.keys():
               solver_options[solver][opt] = option[val]
            else:
               tmp.append(opt)
       for opt in tmp:
         del solver_options[solver][opt]
  return (factor,option,solvers,solver_options)



class FactorFilter(XMLObjectBase):
    def __init__(self, node=None):
        XMLObjectBase.__init__(self)
        self.filter_list = {}
        self.treatment_fn = None
        self.treatment_value = "name"
        self.comparison="name"
        self._python_code = None
        if node is not None:
           self.initialize(node)

    def parse_xml(self,node):
        for child in node.childNodes:
          if child.nodeType == Node.ELEMENT_NODE and child.nodeName.lower() == "factor":
             for (name,value) in child.attributes.items():
               if name == "name":
                  fname = str(value)
               if name == "comparison":
                  self.comparison = str(value)
             self.filter_list[fname] = str(get_xml_text(child))
          elif child.nodeType == Node.ELEMENT_NODE and child.nodeName.lower() == "treatment":
             for (name,value) in child.attributes.items():
               if name == "value":
                  self.treatment_value = str(value)
             self.treatment_fn = str(get_xml_text(child))
          elif child.nodeType == Node.ELEMENT_NODE and child.nodeName.lower() == "python":
             self._python_code = get_xml_text(child)
             #print "Importing module " + self._python_code
             try:
               setattr(self,self._python_code, __import__(self._python_code,globals(),locals(),['']))
             except ImportError:
               print "Problem importing module " + self._python_code
               raise


    def verify_treatment(self,level_name):
        """
        Return True if this TreatmentCombination is not filtered
        """
        if self.treatment_fn is not None:
           #print "HERE verify_treatment"
           add_method(self,eval("self."+self.treatment_fn),"tmp_treatment_fn")
           val = self.tmp_treatment_fn(level_name)
           if not val:
              return False
        return True


    def verify(self,combination):
        """
        Return True if this TreatmentCombination is not filtered
        """
        for (factor,reg_expression) in self.filter_list.items():
          if re.search(reg_expression, combination.levelName(factor)) is None:
             return False
        return True


    def keys(self):
        return self.filter_list.keys()


    def tmp_filter_fn(self,name,value):
        return False

    def test(self,name,level):
        if self.comparison == "exec":
           add_method(self,eval("self."+self.filter_list[name]),"tmp_filter_fn")
           return self.tmp_filter_fn(level.name,level.text)
        if self.comparison == "value":
           tmp = level.text
        else:
           tmp = level.name
        #print "Filter: ",filter[factor.name],"name:",tmp
        return re.search(self.filter_list[name], tmp)


    def apply(self,factor):
        if factor.name in self.filter_list.keys():
           res = []
           for level in factor.levels:
             if self.comparison=="value":
                tmp = level.text
             else:
                tmp = level.name
             #print "Filter: ",self.filter_list[factor.name],"name:",tmp
             if re.search(self.filter_list[factor.name], tmp):
                res.append(level)
           return res
        return factor.levels



class Measurement:
    def __init__(self,type,value):
        self.type=type
        self.value=value


class ExperimentalTrial(object):
    def __init__(self, node=None):
        """
        An object that contains experimental results for a single 
        trial
        """
        self.reset()
        if node:
           self.initialize(node)


    def reset(self):
        self.id = -1
        self.seed = -1
        self.value = {}


    def initialize(self, node):
        self.reset()
        for (name,value) in node.attributes.items():
          if name == "id":
             self.id = value
          elif name == "seed":
             self.seed = value
        for child in node.childNodes:
          if child.nodeType == Node.ELEMENT_NODE and child.nodeName.lower() == "value":
             vname = "unknown"
             vtype = "unknown"
             for (name,value) in child.attributes.items():
               if name == "name":
                  vname = str(value)
               elif name == "type":
                  vtype = value
             vtext = get_xml_text(child)
             if (vtype == "numeric/double" or vtype == "numeric/integer" or\
                 vtype == "numeric/boolean") and (vtext != "ERROR"):
                try:
                  #print "HERE",vname,vtype,self.value
                  if vtype == "numeric/boolean":
                     self.value[vname] = Measurement(vtype, eval("bool(" + vtext + ")"))
                  elif vtext == "Infinity" or vtext == "Inf":
                     self.value[vname] = Measurement(vtype, 1e308)
                  elif vtext == "-Infinity" or vtext == "-Inf":
                     self.value[vname] = Measurement(vtype, -1e308)
                  else:
                     self.value[vname] = Measurement(vtype, eval(vtext))
                except:
                  print "ERROR: problem evaluating value " + vtext + " which is of type " + vtype
                  raise
             else:
                self.value[vname] = Measurement(vtype, vtext)


    def pprint(self,prefix=""):
        print prefix + "id=" + self.id + " seed=" + self.seed,
        vkeys = self.value.keys()
        vkeys.sort()
        for vname in vkeys:
          foo = vname + "="
          tmp = self.value[vname].value
          if isinstance(tmp,types.StringType) or isinstance(tmp,types.UnicodeType):
             foo = foo + "\"" + self.value[vname].value.strip() + "\""
          else:
             foo = foo + `tmp`
          print foo,
        print ""


    def keys(self):
        return self.value.keys() + ['seed', 'id']

    def measurements(self):
        return self.value.keys() + ['seed', 'id']


    def __getitem__(self,index):
        try:
           if index == "seed":
              return self.seed
           elif index == "id":
              return self.id
           return self.value[index]
        except KeyError, info:
           print "Bad key for trial measurement: " + index
           print "Valid keys are " + `self.value.keys()`
           sys.exit(0)




class TreatmentCombination(object):
    def __init__(self, node=None):
        """
        An object that contains experimental results for a single 
        treatment combination (i.e. combination of factor levels)
        """
        self.reset()
        if node:
           self.initialize(node)


    def reset(self):
        self.name = "unknown"
        self.start_time = ""
        self.run_time = -1.0
        self.expparams = ""
        self.level_name = {}  # factor_name -> level_name
        self.level_text = {}  # factor_name -> level_text
        self.replicationlist = []
        self.measurements_set = set()
        self.key = None
        self.status = "Fail"


    def measurements(self):
        return self.measurements_set


    def tuple_key(self):
        return flatten_dict(self.level_name)


    def levelName(self, factor_name):
        try:
          return self.level_name[factor_name]
        except KeyError:
          if not factor_name:
             print "ERROR: factor name is not specified!"
          else:
             print "ERROR: factor name \"" + factor_name + "\" is not valid: " + self.level_name.keys()
          raise


    def levelText(self, factor_name):
        return self.level_text[factor_name]


    def initialize(self, node):
        """
        Initialize a treatment condition with a node of an XML parsed tree.
        """
        self.reset()
        for child in node.childNodes:
          if child.nodeType == Node.ELEMENT_NODE:
             cnode_name = child.nodeName.lower()
             if cnode_name == "starttime":
                self.start_time = get_xml_text(child)

             elif cnode_name == "name":
                self.name = get_xml_text(child)

             elif cnode_name == "runtime":
                self.run_time = get_xml_text(child)

             elif cnode_name == "executionstatus":
                self.status = get_xml_text(child)

             elif cnode_name == "description":
                self.expparams = get_xml_text(child)
                for fnode in child.childNodes:
                  if fnode.nodeType == Node.ELEMENT_NODE and\
                     fnode.nodeName.lower() == "factor":
                     #
                     # Setup a diagnostic text string
                     #
                     ftext = get_xml_text(fnode)
                     self.expparams = self.expparams + " " + ftext
                     #
                     # Get the factor levels
                     #
                     fname = ""
                     flevel = -1
                     for (name,value) in fnode.attributes.items():
                       if name == "name":
                          fname = str(value)
                       elif name == "level":
                          flevel = value
                     self.level_name[fname] = flevel
                     self.level_text[fname] = ftext

             elif cnode_name == "trial":
                tmp = ExperimentalTrial(child)
                self.measurements_set.update(tmp.measurements())
                self.replicationlist.append(tmp)


    def numReplications(self):
        return len(self.replicationlist)


    def replication(self,num):
        return self.replicationlist[num]


    def __len__(self):
        return len(self.replicationlist)


    def __iter__(self):
        """
        Returns the iterator to the replication list.  This method allows
        a TreatmentCombinations() object to be treated as the generator for the 
        iterator of the list of ExperimentalTrial().
        """
        return self.replicationlist.__iter__()


    def __getitem__(self,index):
        """
        Returns the index-th replication
        """
        return self.replicationlist[index]


    def pprint(self,prefix=""):
        print prefix+"Treatment Combination: " + self.name
        print prefix+"  Start Time:          " + self.start_time
        print prefix+"  Run Time:            " + self.run_time
        print prefix+"  Status:              " + self.status
        print prefix+"  Levels:"
        for name in self.level_name.keys():
          print prefix+"        " + name + "\t" + self.level_name[name] + " : " + self.level_text[name]
        print prefix+"  Exp Params:          \"" + self.expparams.strip() + "\""
        print prefix+"  Trials:"
        for trial in self.replicationlist:
          trial.pprint(prefix+"  ")




class ExperimentalResults(XMLObjectBase):
    def __init__(self, node=None, path=None):
        """
        An object that describes experimental results.
        """
        XMLObjectBase.__init__(self)
        self.reset()
        self.path = path
        if node:
           self.initialize(node)


    def reset(self):
        self.combinations = []
        self.measurements_set = set()
        self.comb_dict = {}    # flattened_comb -> index
        XMLObjectBase.reset(self)


    def parse_xml(self, node):
        """
        Initialize the experimental results with a node of an XML parsed tree.
        """
        self.reset()
        for child in node.childNodes:
          if child.nodeType == Node.ELEMENT_NODE and child.nodeName.lower() == "experiment":
             tc = TreatmentCombination(child)
             self.measurements_set.update(tc.measurements())
             self.combinations.append(tc)
             self.comb_dict[tc.tuple_key()] = len(self.combinations)-1
            
    def measurements(self):
        return self.measurements_set

    def __iter__(self):
        """
        Returns the iterator to the combination list.  This method allows
        a ExperimentalResults() object to be treated as the generator for the 
        iterator of the list of ExperimentalCombination().
        """
        return self.combinations.__iter__()


    def __getitem__(self,index):
        """
        Given a list or tuple of factor_name/level_name pairs, return the
        corresponding combination
        """
        if isinstance(index,list):
           #
           # Simply create a tuple from a list of factor/level pairs
           #
           tmp = tuple(index)
        elif isinstance(index,TreatmentCombination):
           #
           # Create a tuple from the dictionary of factor/level pairs
           # in a treatment combination
           #
           tmp = tuple(index.tuple_key())
        else:
           #
           # Rename the tuple index for convenience
           #
           tmp = index
        return self.combinations[self.comb_dict[tmp]]


    def __len__(self):
        """
        Returns the number of experimental combinations in this object.
        """
        return len(self.combinations)


    def __contains__(self, item):
        """
        Returns true if this is a combination object whose
        key matches one of the keys of the combinations in this
        experimental results object.
        """
        if isinstance(item,TreatmentCombination):
           return item.tuple_key() in self.comb_dict.keys()
        return False

        
    def pprint(self,prefix=""):
        for combination in self.combinations:
          combination.pprint(prefix)


    def factorNames(self):
        factors = self.combinations[0].level_name.keys()
        factors.sort()
        return factors

    def levelNames(self, factor_name):
        tmp = {}
        for combination in self.combinations:
          tmp[combination.levelName(factor_name)] = 1;
        #
        # Return keys in sorted order to make things pretty
        #
        keys = tmp.keys()
        keys.sort()
        return keys


    def combinationSubsets(self, factor_list):
        ans = []
        subsets=set()
        factor_list.sort()
        i = 0
        for combination in self.combinations:
          tmp = combination.level_name.copy()
          for factor in factor_list:
            tmp[factor] = '*'
          subset_tuple = flatten_dict(tmp)
          if subset_tuple not in subsets:
             subsets = subsets.union(set([subset_tuple]))
             ans.append(list(subset_tuple))
          i = i + 1
        return ans
          




class FactorLevel(object):
    def __init__(self, node=None, number=None):
        """
        An object describes a factor level for an experiment.  This is
        simply a list of FactorLevel objects
        """
        self.reset()
        if node:
           self.initialize(node,number)

    def reset(self):
        self.attr = {}
        self.name = "unknown"
        self.text = ""
        self.number = -1


    def initialize(self, node, number):
        """
        Initialize the factor level with a node of an XML parsed tree.
        """
        self.reset()
        self.number = number
        if isinstance(node,types.StringType) or isinstance(node,types.UnicodeType):
           self.text = node
           self.name = "level_" + `number`
           #
           # Look for the a token of the form "_level_name=" in the level definition.
           # If it exists, use it to define the level name.
           #
           for token in re.split('[ \t]+',self.text):
             if token[0:12] == "_level_name=":
                self.name = token[12:len(token)]
        else:
          for (name,value) in node.attributes.items():
            self.attr[name] = value
          if self.attr.has_key("name"):
             self.name = self.attr["name"]
          if self.name == "unknown":
             self.name = "level_" + `number`
          for cnode in node.childNodes:
            if cnode.nodeType == Node.TEXT_NODE:
               self.text = self.text + cnode.nodeValue
          self.text.strip()



class Factor(object):
    def __init__(self, node=None, number=None):
        """
        An object describes a factor for an experiment.  This is
        simply a list of FactorLevel objects
        """
        self.reset()
        if node and number:
           self.initialize(node,number)


    def reset(self):
        self.levels = []
        self.level_map = {}
        self.attr = {}
        self.name = "unknown"
        self.number = -1


    def add_level(self,level):
        self.level_map[level.name] = level.number
        self.levels.append(level)


    def level_names(self):
        return self.level_map.keys()


    def initialize(self, node, number):
        """
        Initialize the factor with a node of an XML parsed tree.
        """
        self.reset()
        self.number = number
        for (name,value) in node.attributes.items():
          self.attr[name] = value
        if self.attr.has_key("name"):
           self.name = self.attr["name"]
        if self.name == "unknown":
           self.name = "factor_" + `number`
        if self.attr.has_key("filename"):
           #
           # Read factor levels from a file
           #
           #self.read_factor_levels(self.attr["filename"])
           INPUT = open(self.attr["filename"])
           self.i = 1
           for line in INPUT:
             if line[0] == "#":
                continue
             level = FactorLevel(line.strip(),self.i)
             self.add_level(level)
             self.i = self.i + 1
           INPUT.close()
        else:
           #
           # Initialize factor levels from nodes of an XML parsed tree.
           #
           self.i = 1
           for cnode in node.childNodes:
             if cnode.nodeType == Node.ELEMENT_NODE:
                self.levels.append( FactorLevel(cnode,self.i) )
             self.i = self.i + 1


    def pprint(self,prefix=""):
        print prefix+"Factor " + self.name + " (" + `self.number` + ")"
        for level in self.levels:
          print prefix+"  Level: ",
          if level.name != "unknown":
             print level.name
          else:
             print ""
          print prefix+"    \"" + level.text + "\""


    def apply(self,filter):
        factor = Factor()
        factor.name = self.name
        factor.attr = self.attr
        factor.number = self.number
        if factor.name not in filter.keys():
           for level in self.levels:
             factor.add_level(level)
           return factor
        for level in self.levels:
          if filter.test(factor.name,level):
             factor.add_level(level)
        return factor

    def __len__(self):
        """
        Returns the number of levels in this object.
        """
        return len(self.levels)


    def __iter__(self):
        """
        Returns the iterator to the level list.  This method allows
        a Factor() object to be treated as the generator for the 
        iterator of the list of Levels().
        """
        return self.levels.__iter__()


    def __getitem__(self,index):
        """
        Returns the index-th level
        """
        return self.levels[index]




class Factors(object):
    def __init__(self, node=None):
        """
        An object that describes the factors for an experiment.  This is
        simply a list of Factor objects
        """
        self.reset()
        if node:
           self.initialize(node)


    def reset(self):
        self.factorlist = []


    def initialize(self, node):
        """
        Initialize the factor list with a node of an XML parsed tree.
        """
        self.reset()
        for cnode in node.childNodes:
          if cnode.nodeType == Node.ELEMENT_NODE:
             self.factorlist.append( Factor(cnode,len(self.factorlist)+1) )


    def apply(self,filter):
        factors = Factors()
        for factor in self.factorlist:
          factors.factorlist.append(factor.apply(filter))
        return factors


    def __len__(self):
        """
        Returns the number of factors in this object.
        """
        return len(self.factorlist)


    def __iter__(self):
        """
        Returns the iterator to the factor list.  This method allows
        a Factors() object to be treated as the generator for the 
        iterator of the list of Factors().
        """
        return self.factorlist.__iter__()


    def __getitem__(self,index):
        """
        Returns the index-th factor
        """
        return self.factorlist[index]




class Controls(object):
    def __init__(self, node=None):
        """
        An object that describes the controls for an experiment.
        """
        self.reset()
        if node:
           self.initialize(node)


    def reset(self):
        self.seeds = []
        #
        # EXACT now enforces a default timelimit of 600 seconds (10 min)
        #
        self.timelimit = 600
        self.doe = None
        self.filter = FactorFilter()
        self.executable = ""
        self.executable_type = "default"
        self.replications = 0
        self.driver = None


    def read_seeds(self,name):
          seeds = []
          INPUT = open(name,"r")
          for line in INPUT:
              if line[0] == "#":
                    continue
              for seed in re.split('[ \t]+',line.strip()):
                seeds.append( eval(seed) )
          INPUT.close()
          return seeds


    def initialize(self, node):
        """
        Initialize the experimental controls with a node of an XML parsed tree.
        """
        self.reset()
        for child in node.childNodes:
          if child.nodeType == Node.ELEMENT_NODE:
            #
            # Get replication info
            #
            if child.nodeName.lower() == "replication":
               if get_xml_text(child) != "":
                  tmp = get_xml_text(child)
                  if not isint(tmp):
                     raise IOError, "ERROR: replication value is not a number: \"" + tmp + "\""
                  self.replications=eval(tmp.strip())
               for gchild in child.childNodes:
                  if gchild.nodeType == Node.ELEMENT_NODE and\
                     gchild.nodeName.lower() == "seeds":
                     tmp = get_xml_text(gchild)
                     if tmp != "":
                        self.seeds = re.split('[ \t]+', tmp.strip())
                     if "filename" in gchild.attributes.keys():
                        self.seeds = self.seeds + self.read_seeds(gchild.attributes["filename"].nodeValue)
            elif child.nodeName.lower() == "filter":
               self.filter = FactorFilter(child)
            elif child.nodeName.lower() == "executable":
               self.executable=get_xml_text(child)
               if "type" in child.attributes.keys():
                  self.executable_type = str(child.attributes["type"].nodeValue)
               if "driver" in child.attributes.keys():
                  self.driver = str(child.attributes["driver"].nodeValue)
               if "timelimit" in child.attributes.keys():
                  self.timelimit = eval(child.attributes["timelimit"].nodeValue)
               elif "EXACT_DEFAULT_TIMELIMIT" in os.environ.keys():
                     self.timelimit = eval(os.environ["EXACT_DEFAULT_TIMELIMIT"])
            elif child.nodeName.lower() == "doe":
               self.doe = DesignOfExperiments(child)
        if self.doe == None:
           self.doe = DesignOfExperiments()
        if self.replications == 0:
           self.replications = max(1,len(self.seeds))
        elif len(self.seeds) > 0 and self.replications > len(self.seeds):
           raise IOError, "ERROR: more replications requested than the number of seeds specified."
        if len(self.seeds) == 0:
           for i in range(0,self.replications):
             self.seeds.append(math.ceil(random.random()*1000000))


    def execute(self, name, factors, results, expfile="unknown", force=False):
        if "/" in expfile:
           texpfile = (expfile.split("/"))[-1]
        elif "\\" in expfile:
           texpfile = (expfile.split("\\"))[-1]
        else:
           texpfile = expfile
        #
        # Setup filenames
        #
        tmp = texpfile.split(".")
        if results.path is not None:
           self.path = results.path
        else:
           self.path = ""
        if len(tmp) == 1:
           expname = texpfile + "." + name
           doe_input = self.path + "/" + expname + ".exp.test"
           doe_output = self.path + "/" + expname + ".exp.doe"
           exp_output = expname + ".results.xml"
           seeds_output = self.path + "/" + expname + ".exp.seeds"
        else:
           expname = string.join(tmp[:-2],".") + "." + name
           doe_input = self.path + "/" + expname + ".exp.tmp"
           doe_output = self.path + "/" + expname + ".exp.doe"
           exp_output = expname + ".results.xml"
           seeds_output = self.path + "/" + expname + ".exp.seeds"
        print "      Experiment: " + expname + " ",
        sys.stdout.flush()
        #
        # See if we need to delete previous experimental results
        #
        if self.path != "" and os.path.exists(self.path):
           if force:
              recursive_delete(self.path)
           else:
              print "-- Data already exists"
              return
        if global_data.debug:
           print "Experimental control generating output in directory " + self.path
        if self.path != "":
           os.mkdir(self.path)
        #
        # Write seed file if running a 'runexp_driver' script
        #
        if global_data.debug:
           print "Controls executing with " + self.executable_type + " driver"
        if self.executable_type == "runexp_driver" or\
           self.executable_type == "runexp_simple":
           if len(self.seeds) > 0:
              OUTPUT = open(seeds_output,"w")
              i = 0
              while i < self.replications:
                print >>OUTPUT, self.seeds[i]
                i = i + 1
              OUTPUT.close()
           elif os.path.isfile(seeds_output):
              os.remove(seeds_output)
        #
        # Setup command line
        #
        if "EXACT_DRIVER" in os.environ.keys():
           self.env_driver = os.environ["EXACT_DRIVER"]
        else:
           self.env_driver = None
        if self.driver:
           os.environ["EXACT_DRIVER"] = self.driver
        #
        # Use the existing EXACT_DRIVER environment if 
        # it hasn't been specified in the study file.
        #
        commands.getoutput("(rm -f " + expname + ".*.out) > /dev/null 2>&1")
        #
        # Cleanup old results
        #
        results.reset()
        #
        # Setup DOE
        #
        filtered_factors = self.doe.execute(factors,self.filter)
        if global_data.debug:
           print "Using the following DOE"
           for val in self.doe:
             print "[",
             i = 0
             for item in val:
               print filtered_factors[i][item-1].name,
               i = i + 1
             print "]"
        #
        # Perform execution
        #
        OUTPUT = open(self.path + "/" + exp_output,"w")
        print >>OUTPUT, "<Results expfile=\"" + expfile +"\">"
        id = 1
        for exp in self.doe:
         if self.executable_type == "runexp_driver" or \
            self.executable_type == "runexp_simple":
            #
            # "runexp_driver" is the old-fashioned 'runexp' mechanism
            # "runexp_simple" is the new 'runexp' mechanism, which calls
            #                runexp_expdriver.pl
            #
            if self.executable_type == "runexp_driver":
               cmd = self.executable
            else:
               cmd = "runexp_expdriver.pl --script \"" + self.executable + "\""
            if global_data.debug:
               cmd = cmd + " --debug"
            cmd = cmd + " " + expname + " " + `id` + " " + `self.replications`
            i=1
            for val in exp:
              cmd = cmd + " \"" + filtered_factors[i-1].name + "\""
              cmd = cmd + " \"" + filtered_factors[i-1][val-1].name + "\""
              finfo = filtered_factors[i-1][val-1].text
              cmd = cmd + " \"" + finfo.replace('\"','\\\"') + "\""
              i = i+1
            if global_data.debug:
               print "Executing command:", cmd
            [rc, log] = pyutilib.subprocess.run(cmd, shell=True)
            #process = SubprocessMngr(cmd,stdout=subprocess.PIPE)
            #global_data.current_process = process
            #sys.stdout.flush()
            #process.wait(self.timelimit)
            #global_data.current_process = None
            #log = process.stdout().read()
            sys.stdout.write(".")
            sys.stdout.flush()
            print >>OUTPUT, log
         elif self.executable_type == "default":
            print >>OUTPUT, "<Experiment>"
            #
            # This is the new runexp mechanism, adapted to _not_
            #        call runexp_driver.pl
            #
            # Create the input file for all trials
            #
            self.create_input_file(expname,id,filtered_factors,exp)
            #
            # Execute trials
            #
            # NOTE: this could be done asynchronously!
            #
            stime = clock()
            trial_info = []
            for i in range(0,self.replications):
              #
              # Setup the random number seed
              # 
              os.environ["PSEUDORANDOM_SEED"] = `self.seeds[i]`
              #
              # Execute the i-th trial
              #
              trial_info.append(self.execute_trial(expname,id,i,filtered_factors,exp))
            if not global_data.debug:
               os.unlink(self.path + "/" + expname + "_" + `id` + ".in")
            sys.stdout.write(".")
            sys.stdout.flush()
            rtime = clock() - stime
            print >>OUTPUT, "  <Category>" + expname + "</Category>"
            print >>OUTPUT, "  <Name>" + `id` + "</Name>"
            print >>OUTPUT, "  <StartTime>" + time.ctime(stime) + "</StartTime>"
            print >>OUTPUT, "  <RunTime unit=\"seconds\">" + `rtime` + "</RunTime>"
            print >>OUTPUT, "  <ExecutionStatus>Pass</ExecutionStatus>"
            print >>OUTPUT, "  <Description>"
            for j in range(0,len(filtered_factors)):
              ndx = j+1
              print >>OUTPUT, "    <Factor name=\"" + filtered_factors[j].name + "\"",
              print >>OUTPUT, "level=\"" + filtered_factors[j].levels[exp[j]-1].name + "\">" + filtered_factors[j].levels[exp[j]-1].text + "</Factor>"
            print >>OUTPUT, "  </Description>"
            for info in trial_info:
              print >>OUTPUT, "  <Trial id=\"" + `info.id` + "\" seed=\"" + info.seed + "\">"
              print >>OUTPUT, "    <Status>" + info.status + "</Status>"
              if info.status == "Fail":
                 print >>OUTPUT, "    <Explanation>" + info.explanation + "</Explanation>"
                 
              print >>OUTPUT, "    <Value name=\"LogFile\" type=\"text/string\">" + info.logfile + "</Value>"
              print >>OUTPUT, "    <Value name=\"OutFile\" type=\"text/string\">" + info.outfile + "</Value>"
              if os.path.exists(info.outfile):
                 INPUT = open(info.outfile)
                 state=0
                 for line in INPUT:
                   try:
                     token = quote_split('[ \t]+',line.strip())
                   except ValueError, info:
                     token = re.split('[ \t]+',line.strip())
                     if not ((len(token) == 3 and token[2] == "\"\"\"") or\
                             (len(token) == 1 and token[0] == "\"\"\"")):
                        print "LINE: ", line.strip()
                        raise
                   if state == 1:
                      if line.strip() == "\"\"\"":
                         state=0
                         print >>OUTPUT, "    <Value name=\"" + mname + "\" type=\"" + mtype + "\">" + escape(mval) + "</Value>"
                      else:
                         mval = mval + line
                      continue
                   if len(token) != 3:
                      raise IOError, "Problem parsing line from file \"" + info.outfile + "\"\n" + line
                   if token[2] == "\"\"\"":
                      state = 1
                      mval=""
                      mtype=token[1]
                      mname=token[0]
                      continue
                   if token[0][0] == "\"":
                      token[0] = token[0][1:len(token[0])-1]
                   if token[1] == "text/string" and (token[2][0] == "\"" or token[2][0] == "'"):
                      print >>OUTPUT, "    <Value name=\"" + token[0] + "\" type=\"" + token[1] + "\">" + escape(token[2][1:len(token[2])-1]) + "</Value>"
                   else:
                      print >>OUTPUT, "    <Value name=\"" + token[0] + "\" type=\"" + token[1] + "\">" + escape(token[2]) + "</Value>"
                 INPUT.close()
              print >>OUTPUT, "  </Trial>"
            print >>OUTPUT, "</Experiment>"
         else:
              raise IOError, "Unknown executable type: \"" + self.executable_type + "\""
         id = id + 1
        print ""
        print >>OUTPUT, "</Results>"
        OUTPUT.close()
        #
        # TODO: load these results directly into the python objects
        #        For now, we read these back in from the *results.xml file.
        #
        results.initialize(exp_output)
        #if global_data.debug:
        #   results.pprint()
        #
        # Reset the EXACT_DRIVER environment to the initial
        # value.
        #
        if self.env_driver is not None:
           os.environ["EXACT_DRIVER"] = self.env_driver


    def create_input_file(self, expname, id, factors, exp):
        """
        Create an input file for the experimental combination defined in 'exp'
        """
        INFILE = open(self.path + "/" + expname + "_" + `id` + ".in","w")
        #
        # Print misc info
        #
        print >>INFILE, "_exact_debug\t" + `int(global_data.debug)`
        print >>INFILE, "_experiment_name\t" + expname
        print >>INFILE, "_test_name\t" + `id`
        print >>INFILE, "_num_trials\t" + `self.replications`
        print >>INFILE, "seed\t$PSEUDORANDOM_SEED"
        #
        # Print factor information
        #
        options = ""
        for j in range(0,len(factors)):
          ndx = j+1
          print >>INFILE, "_factor_" + `ndx` + "_name\t" + factors[j].name
          print >>INFILE, "_factor_" + `ndx` + "_level\t" + factors[j].levels[exp[j]-1].name
          if "\n" in factors[j].levels[exp[j]-1].text:
             print >>INFILE, "_factor_" + `ndx` + "_value\t\"\"\"" 
             print >>INFILE, factors[j].levels[exp[j]-1].text
             print >>INFILE, "\"\"\""
          else:
             print >>INFILE, "_factor_" + `ndx` + "_value\t" + factors[j].levels[exp[j]-1].text
          options = options + " " + factors[j].levels[exp[j]-1].text
        tokens = quote_split('[ \t\n]+',options)
        #
        # Create table of experimental values
        #
        expval = {}
        for token in tokens:
          if (len(token.split('=')) == 2):
             pvar = str(token.split('=')[0])
             pval = str(token.split('=')[1])
             if pvar[0] == "_":
                if pval == "":
                   raise IOError, "It is illegal to specify _option="
                if pval[0] == "_":
                   raise IOError, "We cannot have option=value where both are experimental values '_name'"
                expval[pvar]=pval
        #
        # Print options from factor levels
        #
        for token in tokens:
          if (len(token.split('=')) == 2):
             pvar = str(token.split('=')[0])
             pval = str(token.split('=')[1])
             if pval == "":
                raise IOError, "It is illegal to specify option="
             if pval[0] != "_":
                print >>INFILE, pvar + "\t" + pval.strip()
             else:
                if pval in expval.keys():
                   print >>INFILE, pvar + "\t" + expval[pval].strip()
          else:
             print >>INFILE, token + "\tExactNone"
           
        INFILE.close()
          
          
    def execute_trial(self, expname, id, i, factors, exp):
        logfile = self.path + "/" + expname + "_" + `id` + "." + `i` + ".log"
        outfile = self.path + "/" + expname + "_" + `id` + "." + `i` + ".out"
        cmd = self.executable
        cmd = cmd + " " + self.path + "/" + expname + "_" + `id` + ".in"
        cmd = cmd + " " + outfile
        cmd = cmd + " " + logfile
        if global_data.debug:
           print "Executing command " + cmd
        #
        # Execute the command.  The global current_process is used
        # to manage interupts.
        #
        tstart = clock()
        [status, output] = pyutilib.subprocess.run(cmd)
        #process = SubprocessMngr(cmd,stdout=subprocess.PIPE)
        #global_data.current_process = process.process
        #sys.stdout.flush()
        #status = process.wait(self.timelimit)
        #global_data.current_process = None
        #output = process.stdout().read()
        telapsed = clock()-tstart
        if status != 0:
           executionstatus = "Fail"
           if status == -1:
              explanation = "Execution may have exceeded EXACT timelimit"
           else:
              explanation = "Unknown execution failure: exit_status=" + `status`
        elif not os.path.isfile(logfile):
           executionstatus = "Fail"
           explanation = "Missing log file " + logfile
        elif not os.path.isfile(outfile):
           executionstatus = "Fail"
           explanation = "Missing output file " + outfile
        elif os.stat(outfile)[6] == 0:
           executionstatus = "Fail"
           explanation = "Empty output file"
        else:
           executionstatus="Pass"
           explanation=""
        if os.path.exists(logfile):
           #
           # Append seed information to the end of the log file
           #
           LOGFILE = open(logfile,"a")
        else:
           LOGFILE = open(logfile,"w")
        print >>LOGFILE, "Seed: " + `eval("int(" + os.environ["PSEUDORANDOM_SEED"] + ")")`
        LOGFILE.close()
        #
        # Create the *log.xml file
        #
        XMLLOGFILE = open(logfile + ".xml", "w")
        print >>XMLLOGFILE, "<TrialOutput>"
        print >>XMLLOGFILE, "<TrialOptions>"
        for j in range(0,len(factors)):
          ndx = j+1
          print >>XMLLOGFILE, "  _factor_" + `ndx` + "_name\t" + factors[j].name
          print >>XMLLOGFILE, "  _factor_" + `ndx` + "_level\t" + factors[j].levels[exp[j]-1].name
          print >>XMLLOGFILE, "  _factor_" + `ndx` + "_value\t\"" + factors[j].levels[exp[j]-1].text + "\""
        print >>XMLLOGFILE, "</TrialOptions>"
        print >>XMLLOGFILE, "<CommandLine>"
        print >>XMLLOGFILE, escape(cmd)
        print >>XMLLOGFILE, "</CommandLine>"
        print >>XMLLOGFILE, "<CommandLog>"
        print >>XMLLOGFILE, escape(output)
        print >>XMLLOGFILE, "</CommandLog>"
        print >>XMLLOGFILE, "<Output>"
        INPUT = open(logfile,'r')
        for line in INPUT:
          print >>XMLLOGFILE, escape(line),
        print >>XMLLOGFILE, "</Output>"
        print >>XMLLOGFILE, "</TrialOutput>"
        XMLLOGFILE.close()
        if not global_data.debug and os.path.exists(logfile):
           os.unlink(logfile)
        return Bunch(time=telapsed, status=executionstatus, \
                        explanation=explanation, \
                        logfile=logfile + ".xml", \
                        outfile=outfile, \
                        id=id, \
                        seed=os.environ["PSEUDORANDOM_SEED"])
           

class Experiment(object):
    def __init__(self, node=None, expnum=None, expname=None, load_results=True, path=None, only_results=False):
        """
        An experiment object, which contains the factors for an
        experiment as well as the experimental results.
        """
        self.path = None
        self.path_prefix = path
        self.only_results = only_results
        if node and expnum:
           self.initialize(node,expnum)
        if expname and load_results:
           try:
              self.readResults(studyname=expname)
           except IOError, info:
              if global_data.debug:
                 print "Warning: could not load results from " + expname
              #
              # TODO: resolve error handling semantics.
              #
              # The default behavior is to try to read in an
              # experimental results file.  It shouldn't be an error
              # if this file doesn't exist, but we should be more careful
              # with our error management here.  The file could have existed,
              # but we had an error parsing/processing it!
              #
              pass


    def reset(self):
        self.name = "unknown"
        self.factors = None
        self.controls = None
        self.results = ExperimentalResults()


    def initialize(self,node,expnum):
        """
        Initialize the experiment with a node of an XML parsed tree.
        """
        self.reset()
        #
        # Setup experiment name
        #
        for (name,value) in node.attributes.items():
          if name == "name":
             self.name = str(value)
        if self.name == "unknown":
           self.name = "exp" + `expnum`
        if self.path_prefix is not None:
           self.path = self.path_prefix + "/" + self.name
        #
        # Process factors and controls if loading XML
        #
        if self.only_results == False:
           for cnode in node.childNodes:
               if cnode.nodeType == Node.ELEMENT_NODE:
                  if cnode.nodeName.lower() == "factors":
                     self.factors = Factors(cnode)
                  elif cnode.nodeName.lower() == "controls":
                     self.controls = Controls(cnode)
                  elif cnode.nodeName.lower() == "path":
                     if self.path is None:
                        self.path = str(get_xml_text(cnode))
                        self.path = self.path.strip()
           if self.path is not None:
              self.results.path = self.path


    def readResults(self, studyname=None, filename=None):
        if filename is not None:
           fname = filename
        else:
           fname = self.path + "/" + studyname + "." + self.name + ".results.xml"
        if not os.path.exists(fname):
           raise IOError, "Unable to load file " + fname + " ... does not exist"
        if global_data.debug:
           print "  ... loading results file " + fname
        doc = minidom.parse(fname)
        self.results = ExperimentalResults(doc.documentElement,self.path)
        if self.results == None:
           raise IOError, "readResults() did not read any results"


    def execute(self,factorlist=[],expfilename="unknown",force=False):
        if len(factorlist) > 0:
           #
           # The experimental design is simply a single experiment specified
           # by the user.  (Note: user _must_ use named factor levels)
           #
           # NOTE: this code is not currently being exercised within exact
           #
           if len(factorlist) != len(factors):
              print "ERROR: expected " + `len(factors)` + " factors but the user specified " + `len(factorlist)`
              sys.exit(1)
           i = 0
           for level in factorlist:
             if level not in factors[i].level_names():
                print ""
                print "ERROR: invalid level for factor " + `i` + " : " + level
                print "ERROR: Factor Levels: ",
                for factor in factors:
                  print " " + `len(factor)` + " " + `factor.level_names()`
                print " "
                sys.exit(1)
             i = i + 1
           self.controls.doe.set([ self.factors ])
        self.controls.execute(self.name, self.factors, self.results, expfilename, force=force)
        return


    def pprint(self,prefix=""):
        if self.factors:
          print prefix+"Factors: " + `len(self.factors.factorlist)`
          for factor in self.factors:
            factor.pprint(prefix+"  ")
        else:
          print prefix+"Factors: " + "None"
        print prefix+"Results:"
        if self.results:
           self.results.pprint(prefix+"  ")
        else:
           print prefix+"  None"


