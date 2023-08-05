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
import time
import copy
from exact_xml import *
from misc_utilities import *
from exact_globals import *
from experiment import FactorFilter
from experiment import Measurement
import commands
from pyutilib.misc import get_xml_text, Bunch, quote_split, escape, add_method
from pyutilib.math import mean, median


#
# A function that parses an XML node, and returns an Analysis object
# that has been initialized with that node
#
def Analysis(node, path, load_results=False,only_results=False,study="none",key=None):
        analysis_name = "unknown"
        type = "unknown"
        for (name,value) in node.attributes.items():
          tmp = name.lower()
          if tmp == "type":
             type = value
          elif tmp == "name":
             analysis_name = value
        #XXX print "type = ", type,  " val ", value   # syc
        if type == "unknown":
           raise IOError, "Unknown analysis type for analysis block \"" + analysis_name + "\""
        if type not in global_data.analysis_factory:
           msg = "Unknown analysis type \"" + type + "\" for analysis block \"" + analysis_name + "\"\nValid analysis types:"
           for key in global_data.analysis_factory.keys():
             msg = msg + " " + key
           raise IOError, msg
        object = global_data.analysis_factory.construct(type)
        object.path = path
        object._load_results = load_results
        object._only_results = only_results
        object._studyname=study
        object._key=key
        object.initialize(node)
        return object


#
# A base python class for analysis objects
#
class AnalysisBase(object):
    def __init__(self, node=None):
        self._name = "unknown"
        self._data = [ Bunch(experiment="exp1", expimport=None, filter=FactorFilter(), results_file=None) ]
        self._options = ""
        self.option_dict = {}
        self._extravars = []        # variables from parser to always print in analysis
        self._extras = {}        # storage for these variables
        self._python_code = ""
        self._type = ""
        self._categories = ["default"]
        if node:
           self.initialize(node)


    def num_tests(self, status=None):
        #raise IOError, "num_tests undefined in analysis"
        return 0


    def execute(self, exps, print_summary=True, force=False, expstudy="unknown"):
        raise IOError, "execute undefined in analysis"
        pass


    # Method used to customize the initialization of 
    # analysis elements.
    def initialize_callback(self, node):
        pass

    def initialize(self, node):
        for (name,value) in node.attributes.items():
          tmp = name.lower()
          if tmp == "type":
             self._type = value
          elif tmp == "name":
             self._name = value
        if self._load_results:
           self.readResults()
        for cnode in node.childNodes:
          if cnode.nodeType == Node.ELEMENT_NODE:
             cnode_name = cnode.nodeName.lower()
             if cnode_name == "category":
                if self._categories == ["default"]:
                   self._categories = [get_xml_text(cnode)]
                else:
                   self._categories.append(get_xml_text(cnode))
        if self._only_results:
           return
        data = []
        for cnode in node.childNodes:
          if cnode.nodeType == Node.ELEMENT_NODE:
             cnode_name = cnode.nodeName.lower()
             if cnode_name == "data":
                expname = "exp1"
                importname = None
                results_file = None
                for (name,value) in cnode.attributes.items():
                  if name.lower() == "experiment":
                     expname = str(value)
                  elif name.lower() == "import":
                     importname = str(value)
                  elif name.lower() == "results":
                     results_file = str(value)
                filter=None
                for gnode in cnode.childNodes:
                  if gnode.nodeType == Node.ELEMENT_NODE and gnode.nodeName.lower() == "filter":
                     filter = FactorFilter(gnode)
                data = data + [ Bunch(experiment=expname, expimport=importname, filter=filter, results_file=results_file) ]
             elif cnode_name == "options":
                self._options = get_xml_text(cnode)
             elif cnode_name == "python":
                self._python_code = get_xml_text(cnode)
                try:
                   setattr(self,self._python_code, __import__(self._python_code,globals(),locals(),['']))
                except ImportError:
                   print "Problem importing module " + self._python_code
                   raise
             else:
                 self.initialize_callback(cnode)
        if len(data) > 0:
           self._data = data


    def xml_filename(self, expstudy):
        fname = self.path + "/" + expstudy + "." + self._name + ".analysis.xml"
        return str(fname)

    def junit_xml_filename(self, expstudy):
        fname = self.path + "/TEST-" + expstudy + "." + self._name + ".xml"
        return str(fname)

    def readResults(self, expstudy=""):
        fname = self.xml_filename(expstudy)
        if not os.path.exists(fname):
           raise IOError, "Unable to load file " + fname + " ... does not exist"
        if global_data.debug:
           print "  ... loading results file " + fname
        self._filename = fname
        doc = minidom.parse(fname)
        for cnode in doc.documentElement.childNodes:
          if cnode.nodeType == Node.ELEMENT_NODE:
             cnode_name = cnode.nodeName.lower()
             if cnode_name == "results":
                self.read_analysis_results(cnode)


    def pprint(self, prefix=""):
        # raise IOError, "pprint undefined in analysis"
        # print prefix + "analysis: pprint undefined"
        # pass
        print prefix+"Name: " + self._name
        # print prefix+"Experiment: ", self._data.experiment
        # print prefix+"Expimport: ", self._data.expimport
        # print prefix+"FactorFilter: ", self._data.filter
        # print prefix+"Results: ", self._data.results_file
        print prefix+"Options: ", self._options
        print prefix+"Extravars: ", self._extravars
        print prefix+"Pycode: ", self._python_code
        print prefix+"Type: ", self._type
        print prefix+"Categories: ", self._categories


    def process_options(self, olist):
        self.option_dict = {}
        for ostring in olist:
          if ostring != "":
             tokens = quote_split('[ \t]+',ostring)
             for token in tokens:
               if (len(token.split("=")) == 2):
                 if global_data.debug:
                    print "OPTION: " + token
                 if token[0] in ['_','+','$']:
                    appending = (token[0] == "+")  # +var is a "list" type of var for other uses
                    pyvar = token.split("=")[0]
                    pyval = token.split("=")[1]
                    self.option_dict[pyvar[1:]]=pyval
                    if appending and not hasattr(self, pyvar[1:]):
                       self.__dict__[pyvar[1:]] = []
                    if pyval[0] == "_":
                       if appending:
                         if pyval[1:] not in getattr(self,pyvar[1:]):
                            self.__dict__[pyvar[1:]].append(self.__dict__[pyval[1:]])
                       else:
                          setattr(self,pyvar[1:],self.__dict__[pyval[1:]])
                    elif pyval[0] == "$":
                      tmp_pyval = os.environ[pyval[1:]]
                      if appending:
                        if tmp_pyval not in getattr(self,tmp_pyvar[1:]):
                          self.__dict__[pyvar[1:]].append(tmp_pyval)
                      else:
                        setattr(self,pyvar[1:],tmp_pyval)
                    else:
                      #
                      # Set an attribute in this class with name `pyvar[1:]`
                      #
                      # First try to set the attribute with the eval() of the
                      #        pyval:
                      #                _foo=0.0
                      #                _foo=max
                      #
                      # Second, try to set the attribute with the eval() of
                      #        "self." + pyval:
                      #                _foo=tolerance
                      #
                      # Finally, simply set the attribute to the string pyval
                      #
                      try:
                        tmp = eval(pyval)
                        if isinstance(tmp,types.StringType):
                          try:
                            tmp = eval(tmp)
                          except:
                            pass
                        if appending:
                          if tmp not in getattr(self,pyvar[1:]):
                            self.__dict__[pyvar[1:]].append(tmp)
                        else:
                          setattr(self,pyvar[1:], tmp)
                      except:
                        try:
                          if appending:
                            if eval("self." + pyval) not in getattr(self,pyvar[1:]):
                              self.__dict__[pyvar[1:]].append(eval("self." + pyval))
                          else:
                            setattr(self,pyvar[1:], eval("self." + pyval))
                        except:
                          if appending:
                            if pyval not in list(getattr(self,pyvar[1:])):
                              self.__dict__[pyvar[1:]].append(pyval)
                              #XXX print "option pyvar[1:] =", getattr(self,pyvar[1:]) #syc
                          else:
                            setattr(self,pyvar[1:], pyval)


    def write_xml(self, expstudy="", force=False):
        self.write_exact_xml(expstudy, force)
        self.write_junit_xml(expstudy, force)

    def write_exact_xml(self, expstudy="", force=False):
        fname = self.xml_filename(expstudy)
        if not force and os.path.exists(fname):
           return
        OUTPUT = open(fname,"w")
        print >>OUTPUT, "<AnalysisResults name=\"" + self._name + "\" study=\"" + expstudy + "\" type=\"" + self._type + "\" >"
        for val in self._data:
          print >>OUTPUT, "  <Data",
          if val.expimport:
             print >>OUTPUT, "expimport=\"" + val.expimport + "\"",
          print >>OUTPUT, "experiment=\"" + val.experiment + "\"/>"
        #
        # Write header info
        #
        if self._python_code != "":
           print >>OUTPUT, "  <PythonCode>" + escape(self._python_code) + "</PythonCode>"
        if self._options != "":
           print >>OUTPUT, "  <Options>" + escape(self._options) + "</Options>"
        if len(self._extravars) > 0:
           print >>OUTPUT, "  <ExtraVars>",
           for v in self._extravars:
             print >>OUTPUT, escape(v),
           print >>OUTPUT, "</ExtraVars>"
        print >>OUTPUT, "  <Results>"
        self.write_analysis_results(OUTPUT)
        print >>OUTPUT, "  </Results>"
        print >>OUTPUT, "</AnalysisResults>"
        OUTPUT.close()

    def write_junit_xml(self, expstudy="", force=False):
        fname = self.junit_xml_filename(expstudy)
        if not force and os.path.exists(fname):
           return
        OUTPUT = open(fname,"w")
        print >>OUTPUT, "<?xml version=\"1.0\" encoding=\"UTF-8\"?><testsuite name=\"%s.%s\" tests=\"%d\" errors=\"%d\" failures=\"%d\" time=\"%f\">" % (expstudy, self._name, self.num_tests(), 0, self.num_tests(False), 0.0)

        err_header = "<AnalysisResults name=\"" + self._name + "\" study=\"" + expstudy + "\" type=\"" + self._type + "\" >\n"
        for val in self._data:
          err_header += "  <Data "
          if val.expimport:
             err_header += "expimport=\"" + val.expimport + "\" "
          err_header += "experiment=\"" + val.experiment + "\"/>\n"
        #
        # Write header info
        #
        if self._python_code != "":
           err_header += "  <PythonCode>" + escape(self._python_code) + "</PythonCode>\n"
        if self._options != "":
           err_header += "  <Options>" + escape(self._options) + "</Options>\n"
        if len(self._extravars) > 0:
           err_header += "  <ExtraVars> "
           for v in self._extravars:
             err_header += escape(v)+" "
           err_header += "</ExtraVars>\n"

        self.write_junit_results(OUTPUT, err_header, expstudy+"."+self._name)

        print >>OUTPUT, "</testsuite>"
        OUTPUT.close()


    def write_analysis_results(self,OUTPUT):
        raise IOError, "write_analysis_results undefined in analysis"

    def write_junit_results(self,OUTPUT,header, name):
        pass


    def read_analysis_results(self,node):
        raise IOError, "read_analysis_results undefined in analysis"


def compare_fn_default(self, sense, newval, value, tol, cmp_operator):
    """
    The default comparison function
    """
    #print "HERE",newval,value,(sense*(newval-value)),tol,(sense*(newval-value))-tol,((sense*(newval-value))<=tol),cmp_operator

    if cmp_operator == "=" or cmp_operator == "eq":
       if abs(newval-value) <= tol:
          return ("",True)

    elif cmp_operator == "<" or cmp_operator == "lt":
       if (sense*(newval-value)) < tol:
          return ("",True)

    elif cmp_operator == "<=" or cmp_operator == "lte" or cmp_operator=="le" or cmp_operator=="leq":
       if (sense*(newval-value)) <= tol:
          return ("",True)

    elif cmp_operator == ">" or cmp_operator == "gt":
       if (sense*(newval-value)) > -tol:
          return ("",True)

    elif cmp_operator == ">=" or cmp_operator == "gte" or cmp_operator=="ge" or cmp_operator=="geq":
       if (sense*(newval-value)) >= -tol:
          return ("",True)
    else:
       raise IOError, "Bad comparison function"

    return ("Bad difference of statistic and target value: " + `newval` + " and " + `value` + " (" + cmp_operator + ")",False)


def validate_fn_default(self, vals, ttype):
        """
        Analyze the trials of an experiment.
        """
        if ttype == "text/string":
           for val in vals:
             if val != self.value:
                return ("Value \"" + val + "\" differs from \"" + self.value + "\"",False)
           return ("",True)
        elif ttype == "numeric/boolean":
           if self.statistic(vals) == self.value:
              return ("",True)
           else:
              return ("Bad boolean statistic",False)
        elif (ttype == "numeric/double") or (ttype == "numeric/integer"):
           if self.ptolerance is not None:
              tol = self.ptolerance * self.value
           else:
              tol = self.tolerance
           return self.compare(self.sense, self.statistic(vals), self.value, tol, self.cmp_operator)
        return ("Unknown type: " + ttype,False)


#
# This class illustrates how we can define objects to perform
# analysis.  The 'validation' analysis is the simplest form.  It verifies
# that the specified measurement has a given value (within a specified
# tolerance).
#
class ValidationAnalysis(AnalysisBase):
    def __init__(self,node=None):
        """
        An object that can analyze an experiment to validate one
        or more values in the experiment.
        """
        self.measurement=None
        AnalysisBase.value=None
        self.ptolerance=None
        self.tolerance=0.0
        self.opttol=0.0
        self.test_status={}
        self.test_explanation={}
        self.results={}
        self.filter={}
        self.sense=1.0
        self.statistic=max
        self.cmp_operator="<"
        self.test_exit_status=True
        #
        # sense = 1  if minimizing
        # sense = -1 if maximizing
        # sense = 0  if looking for an absolute tolerance level
        #
        self.sense=1.0
        AnalysisBase.__init__(self,node)
        #
        # feedback from parser: exit_comment if it's set
        self._extravars=['exit_comment']


    def num_tests(self, status=None):
        num=0
        #print "HERE - Validation",len(self.test_status)
        for tstatus in self.test_status.values():
            for value in tstatus.values():
              if status is None or value == status:
                 num=num+1
        return num


    def process_options(self, olist):
        """
        Process a list of option/value pairs
        """
        self.value=None
        self.compare_fn=None
        self.validation_method=None

        AnalysisBase.process_options(self,olist)
        if self.value is None:
           self.value=self.optimum
        #self.statistic_fn = add_method(self,self.statistic,self.statistic.__name__+"_statistic")

        if self.validation_method is not None:
           add_method(self,self.validation_method,"validate")
        else:
           add_method(self,validate_fn_default,"validate")
        if self.compare_fn is not None:
           if isinstance(self.compare_fn,types.StringType):
              print "   ERROR: comparison function",self.compare_fn,"not found!"
              return
           add_method(self,self.compare_fn,"compare")
        else:
           add_method(self,compare_fn_default,"compare")

    def execute(self, exps, print_summary=True, force=False, expstudy="unknown"):
        """
        Analyze an experiment.
        """
        if len(self._data) == 0:
           raise ValueError, "Undefined experiment name(s)"
        for i in self._data:
          if print_summary:
             print "      Analysis:   " + self._name + "." + i.experiment + " ",
          if not force and os.path.exists(self.xml_filename(expstudy)):
             print " -- XML output already exists"
          else:
             self.execute_analysis(exps[i.experiment].results, print_summary, i.experiment, i.filter)

    def execute_analysis(self, res, print_summary, expname, filter):
        self.test_status[expname] = {}
        self.test_explanation[expname] = {}
        self.results[expname] = res
        self.filter[expname] = filter
        for combination in self.results[expname]:
          if filter is not None and not filter.verify(combination):
             continue
          self.process_options([combination.expparams, self._options])
          # build up list of optional vars to print in analysis results
          ev = self._extravars[:]
          if hasattr(self, "var"):
            for e in self.var:
              ev.append(e)
          if global_data.debug:
            print "Extravar: ", ev
          for e in ev:
            if self._extras.has_key(e):
              if self._extras[e].has_key(expname):
                self._extras[e][expname][combination.name] = None
              else:
                self._extras[e][expname] = {combination.name: None}
            else:
              self._extras[e] = { expname : { combination.name : None } }

          if not self.measurement:
             raise ValueError, "Undefined measurement type"
          if len(combination) == 0:
             explanation = "No results for experimental trials"
             status = False
          else:
             status = True
             vals = []
             for trial in combination:
               if self.test_exit_status:
                  if not ('exit_status' in trial.keys() and\
                     trial['exit_status'].value == 0):
                     explanation = "Missing or bad exit_status from parser"
                     status = False
                     break
               tvalue = trial[self.measurement].value
               ttype  = trial[self.measurement].type
               for e in ev:
                 if e in trial.keys():
                    if global_data.debug:
                      print "Set extravar", e,"[",expname,"][",combination.name,"] =", trial[e].value
                    self._extras[e][expname][combination.name] = trial[e].value
               if (tvalue == "ERROR") or (tvalue == ""):
                  explanation = "Bad measurement value: \"" + tvalue + "\""
                  status = False
                  break
               vals = vals + [tvalue]
             if status == True:
                (explanation,status) = self.validate(vals,ttype)
          if print_summary:
             if status == True:
                sys.stdout.write(".")
             else:
                sys.stdout.write("F")
          #XXX print self._extras                #syc
          sys.stdout.flush()
          self.test_status[expname][combination.name] = status
          self.test_explanation[expname][combination.name] = explanation
        print ""
        if print_summary:
           for combination in self.results[expname]:
             if filter is not None and not filter.verify(combination):
                continue
             if self.test_status[expname][combination.name] == False:
                print "        ID=" + combination.name + " Comb=",
                for val in combination.tuple_key():
                  print val,
                print ""
                print "           " + self.test_explanation[expname][combination.name]
                for e in self._extras.keys():
                  try:
                    if self._extras[e][expname][combination.name]:
                      print "           " + e + "=" + str(self._extras[e][expname][combination.name])
                  except KeyError:
                    pass

    def write_analysis_results(self,OUTPUT):
        for expname in self.results.keys():
          for combination in self.results[expname]:
            if self.filter[expname] is not None and not self.filter[expname].verify(combination):
               continue
            print >>OUTPUT, "   <Test experiment=\"" + expname + "\" id=\"" + combination.name + "\">"
            print >>OUTPUT, "     <Options>"
            print >>OUTPUT, "     " + combination.expparams.strip()
            print >>OUTPUT, "     </Options>"

            if len(self._extras.keys()) > 0:
              print >>OUTPUT, "     <ExtraVars>"
              varstr = ""
              for var in self._extras.keys():
                try:
                  if (self._extras[var][expname][combination.name]):
                    varstr = "       <Var name=\"" + escape(var) + "\">"
                    varstr = varstr + escape(str(self._extras[var][expname][combination.name]))
                    varstr = varstr + "</Var>"
                    print >>OUTPUT, varstr
                except (NameError,KeyError), e:
                  #XXX print "Var error", e, var, combination.name
                  pass
              print >>OUTPUT, "     </ExtraVars>"
            if self.test_status[expname][combination.name] == True:
               print >>OUTPUT, "     <Status>Pass</Status>"
            else:
               print >>OUTPUT, "     <Status>Fail</Status>"
            print >>OUTPUT, "   </Test>"


    def write_junit_results(self, OUTPUT, header, name):
        for expname in self.results.keys():
          for combination in self.results[expname]:
            if self.filter[expname] is not None and not self.filter[expname].verify(combination):
               continue
            print >>OUTPUT, "   <testcase classname=\"%s\" name=\"%s.%s\" time=\"0.0\">" % (name, expname,combination.name)
            if self.test_status[expname][combination.name] != True:
                print >>OUTPUT, "     <failure>"
            print >>OUTPUT, "     <![CDATA["
            print >>OUTPUT, header
            print >>OUTPUT, "     <Options>"
            print >>OUTPUT, "     " + combination.expparams.strip()
            print >>OUTPUT, "     </Options>"

            if len(self._extras.keys()) > 0:
              print >>OUTPUT, "     <ExtraVars>"
              varstr = ""
              for var in self._extras.keys():
                try:
                  if (self._extras[var][expname][combination.name]):
                    varstr = "       <Var name=\"" + escape(var) + "\">"
                    varstr = varstr + escape(str(self._extras[var][expname][combination.name]))
                    varstr = varstr + "</Var>"
                    print >>OUTPUT, varstr
                except (NameError,KeyError), e:
                  pass
              print >>OUTPUT, "     </ExtraVars>"
            if self.test_status[expname][combination.name] == True:
               print >>OUTPUT, "     ]]>"
            else:
               print >>OUTPUT, "     ]]></failure>"
            print >>OUTPUT, "   </testcase>"


    def read_analysis_results(self,node):
        for cnode in node.childNodes:
          if cnode.nodeType == Node.ELEMENT_NODE:
             cnode_name = cnode.nodeName.lower()
             if cnode_name == "test":
                expname=""
                comb=""
                for (name,value) in cnode.attributes.items():
                  if name == "experiment":
                          expname=value
                  elif name == "id":
                     comb=value
                if expname not in self.test_status.keys():
                   self.test_status[expname] = {}
                for gnode in cnode.childNodes:
                  if gnode.nodeType == Node.ELEMENT_NODE:
                     gnode_name = gnode.nodeName.lower()
                     if gnode_name == "status":
                        value = get_xml_text(gnode)
                        self.test_status[expname][comb] = (value == "Pass")




#
# This class illustrates how we can analyze an ExperimentalResults object to 
# compare a slide of results against another.  The final statistics
# are the relative ratio of performance of one slice against the other slices.
#
# The goal of this example is to exercise the interface to ExperimentalResults to
# ensure that results can be flexibly analyzed.
#
class RelativePerformanceAnalysis(AnalysisBase):
    def __init__(self):
        """
        An object that can analyze an experiment to compare
        results with one or more sets of 'reference' experiments.  In this
        case, we assume that all computations are performance within
        the same experiment.
        Note: this comparison is only done w.r.t. the first trial for 
        each treatment combination.
        """
        self.target_factor=None
        self.target_level=None
        self.measurement=None
        self.statistic=mean
        self.total={}
        self.errors={}
        self.ranks={}
        AnalysisBase.__init__(self)

    def process_options(self, olist):
        """
        Process a list of option/value pairs
        """
        AnalysisBase.process_options(self,olist)
        #self.statistic_fn = add_method(self,self.statistic,self.statistic.__name__+"_statistic")

    def execute(self, exps, print_summary=True, force=False, expstudy="unknown"):
        """
        Analyze an experiment.
        """
        #
        # Process options and do error checking
        #
        self.process_options(["", self._options])
        if not self.target_factor:
           raise IOError, "ERROR: target factor not specified"
        if not self.target_level:
           raise IOError, "ERROR: target factor's level not specified"
        if not self.measurement:
           raise IOError, "ERROR: performance measurement not specified"
        #
        # Setup data
        #
        for i in self._data:
          if print_summary:
             print "      Analysis:   " + self._name + "." + i.experiment + " ",
          if not force and os.path.exists(self.xml_filename(expstudy)):
             print " -- XML output already exists"
          else:
             self.execute_analysis(exps[i.experiment].results, print_summary, i.experiment)


    def execute_analysis(self, results, print_summary, expname):
        target_levels = results.levelNames(self.target_factor)
        self.total = {}
        self.errors = {}
        self.ranks = {}
        for level in target_levels:
          self.total[level] = []
          self.errors[level] = []
          self.ranks[level] = []
        #
        # Get subsets of treatment combinations that are orthogonal
        # to the target_factor
        #
        subsets = results.combinationSubsets([self.target_factor])
        for group in subsets:
          #
          # Find the index of the target factor
          #
          i = 0
          while (group[i] != self.target_factor) and (i < len(group)):
            i = i + 2
          if (i >= len(group)):
             print "Bad target_factor: " + self.target_factor
             sys.exit(1)
          i = i + 1
          group[i] = self.target_level
          target_combination = results[group]
          #
          # Compare combination measurements
          #
          # Note: this loops through the data a few more times than is strictly
          # necessary, but my goal was to keep this code simple.
          #
          measurements = []
          status = []
          ndx = {}
          j = 0
          for level in target_levels:
            group[i] = level
            vals = []
            tstatus = []
            for replication in results[group]:
              if self.measurement in replication.keys() and\
                 replication[self.measurement].value != "ERROR" and\
                 replication[self.measurement].value != "":
                 vals = vals + [replication[self.measurement].value]
                 tstatus = tstatus + [replication["exit_status"].value]
            if len(vals) == 0:
               status = status + [1]
               measurements = measurements + ["ERROR"]
            else:
               status = status + [min(tstatus)]
               measurements = measurements + [self.statistic(vals)]
            ndx[level] = j
            j = j + 1
          #
          # This is an O(n^2) algorithm, but we _could_ do this in O(nlogn)
          #
          rank = []
          for level in target_levels:
            ctr1 = 0
            ctr2 = 0
            for level_i in target_levels:
              if (level == level_i):
                 continue
              if (status[ndx[level]] == 0 and (status[ndx[level_i]] == 0 and measurements[ndx[level]] > measurements[ndx[level_i]])) or\
                 (status[ndx[level]] == 1 and status[ndx[level_i]] == 0):
                 ctr1 = ctr1 + 1
              if (status[ndx[level]] == 0 and status[ndx[level_i]] == 0 and measurements[ndx[level]] == measurements[ndx[level_i]]) or\
                 (status[ndx[level]] == 1 and status[ndx[level_i]] == 1):
                 ctr2 = ctr2 + 1
            rank = rank + [ctr1 + ctr2/2.0 + 1]
          #
          # Compute totals ... which are performance ratios relative to the target
          #
          for level in target_levels:
            if level == self.target_level:
               if status[ndx[level]] == 0:
                  self.total[level] = self.total[level] + [1.0]
            elif status[ndx[level]] == 0 and status[ndx[self.target_level]] == 0:
               self.total[level] = self.total[level] + [measurements[ndx[level]]/measurements[ndx[self.target_level]]]
            self.ranks[level] = self.ranks[level] + [rank[ndx[level]]]
            if status[ndx[level]] == 1:
               self.errors[level] = self.errors[level] + [1]
        self.summary = "  SOLVER                               MEAN               MEDIAN\n"
        for level in target_levels:
          if level == self.target_level:
               self.summary = self.summary + "  %-20s %20.3f %20.3f\n" % (level,1.0,1.0)
          else:
               self.summary = self.summary + "  %-20s %20.3f %20.3f\n" % (level,mean(self.total[level]),median(self.total[level]))
               #tmp = self.total[level]
               #tmp.sort()
               #print "  " + `tmp`
        self.summary = self.summary + "\n"
        self.summary = self.summary + "  SOLVER                            %Errors             Avg Rank"
        for level in target_levels:
          if len(self.errors[level]) == 0:
             errs = 0.0
          else:
             errs = mean(self.errors[level])
          self.summary = self.summary + "\n  %-20s %20.3f %20.3f" % (level,100.0*errs,mean(self.ranks[level]))
          #tmp = self.ranks[level]
          #tmp.sort()
          #print "  " + `tmp`
        if print_summary:
           print "\n"+self.summary

    def write_analysis_results(self,OUTPUT):
        print >>OUTPUT, self.summary


#
# The 'baseline' analysis verifies
# that one experiment is "sufficiently similar" to another.
#
class BaselineAnalysis(AnalysisBase):
    def __init__(self,node=None):
        """
        An object that can validate one or more experiments against
        a baseline experiment.
        """
        self.measurement=None
        AnalysisBase.value=None
        self.tolerance=0.0
        self.ptolerance=None
        self.test_status={}
        self.test_explanation={}
        self.results = {}
        self.filter = {}
        #
        # sense = 1  if minimizing
        # sense = -1 if maximizing
        # sense = 0  if looking for an absolute tolerance level
        #
        self.sense=0.0
        AnalysisBase.__init__(self,node)

    def process_options(self, olist):
        """
        Process a list of option/value pairs
        """
        self.validation_method=None
        AnalysisBase.process_options(self,olist)
        if self.validation_method is not None:
           add_method(self,self.validation_method,"validate")

    def execute(self, exps, print_summary=True, force=False, expstudy="unknown"):
        """
        Analyze an experiment.
        """
        self.print_summary = print_summary
        if len(self._data) < 2:
           raise ValueError, "Too few experiment names defined"
        baseline_results = exps[self._data[0].experiment].results
        baseline_filter = exps[self._data[0].experiment].filter
        for i in range(1,len(self._data)):
          if print_summary:
             print "      Analysis:   " + self._name + "." + self._data[i].experiment + " ",
          if not force and os.path.exists(self.xml_filename(expstudy)):
             print " -- XML output already exists"
          else:
             self.execute_analysis(baseline_results, baseline_filter, exps[self._data[i].experiment].results, exps[self._data[i].experiment].filter, self._data[i].experiment)

    def execute_analysis(self, baseline_res, baseline_filter, res, filter, expname):
        self.test_status[expname] = {}
        self.test_explanation[expname] = {}
        self.results[expname] = res
        self.filter[expname] = filter
        for combination in self.results[expname]:
          if filter is not None and not filter.verify(combination):
             continue
          #
          # Iterate through all combinations in the results that we are baselining
          #
          self.process_options([combination.expparams, self._options])
          if not self.measurement:
             raise ValueError, "Undefined measurement type"
          if len(combination) == 0:
             #
             # If the combination has no trials, we treat this as a failure, even if
             # the baseline has no trials.  Thus, we require that the experiment not have
             # failed trials in order to be baselined without any errors.
             #
             explanation = "No results for experimental trials"
             status = "Fail"        
          elif len(baseline_res[combination]) == 0:
             #
             # If the baseline combination has no trials, we also treat this as a failure.
             #
             explanation = "No results for experimental trials in the baseline"
             status = "Fail"        
          elif combination not in baseline_res:
             #
             # If a combination is not in the baseline results, then we treat this as a failure.
             #
             explanation = "Combination is not in the baseline"
             status = "Fail"
          else:
             (explanation,status) = self.validate(combination, baseline_res[combination])
          if self.print_summary:
             if status == "Pass":
                sys.stdout.write(".")
             else:
                sys.stdout.write("F")
             sys.stdout.flush()
          self.test_status[expname][combination.name] = status
          self.test_explanation[expname][combination.name] = explanation
        print ""
        if self.print_summary:
           for combination in self.results[expname]:
             if self.test_status[expname][combination.name] == "Fail":
                print "        ID=" + combination.name + " Comb=",
                for val in combination.tuple_key():
                  print val,
                print ""
                print "           " + self.test_explanation[expname][combination.name]

    #
    # This is the 'default' validation method.  This simply verifies that
    # every trial has the same value as the baseline trial.
    # This method can be overridden
    # in this class by specifying the '_validate_method' option.
    #
    def validate(self, combination, baseline_combination):
        """
        Analyze the trials of an experiment.
        """
        if len(combination) != len(baseline_combination):
           explanation="Number of trials in baseline differs from the new results: baseline=" + `len(baseline_combination)` + " results=" + `len(combination)`
           status="Fail"
        elif combination.replication(0)[self.measurement].type != baseline_combination.replication(0)[self.measurement].type:
           explanation="The measurement types appear to be different: baseline=" + baseline_combination.replication(0)[self.measurement].type + " results=" + combination.replication(0)[self.measurement].type
           status="Fail"
        else:
           explanation=""
           status="Pass"
           for i in range(0,len(combination)):
             if not ('exit_status' in combination[i].keys() and\
                  combination.replication(i)['exit_status'].value == 0):
                  explanation = "Trial " + `i` + " failed."
                  status = "Fail"
                  break
             tvalue = combination[i][self.measurement].value
             ttype  = combination[i][self.measurement].type
             bvalue = baseline_combination[i][self.measurement].value
             if (tvalue == "ERROR") or (tvalue == ""):
                explanation = "Trial " + `i` + " has an erroneous or missing error measurement."
                status = "Fail"
                break
             elif (bvalue == "ERROR") or (bvalue == ""):
                explanation = "Baseline trial " + `i` + " has an erroneous or missing error measurement."
                status = "Fail"
                break
             elif (ttype == "numeric/boolean" or ttype == "") and (tvalue != bvalue):
                explanation = "Trial " + `i` + " has a different value."
                status = "Fail"
                break
             elif (ttype == "numeric/double"):
                if global_data.debug:
                  print "Comparing %f with %f" % (bvalue, tvalue)
                if self.ptolerance is not None:
                   tol = self.ptolerance*bvalue
                else:
                   tol = self.tolerance
                # default explanation, if baseline != measurement
                # checks for significant difference and creates explanation (printed in Passed experiments)
                # Failures will overwrite it with real error explanation
                if (bvalue != 0) and (1 - abs(round(tvalue / bvalue, 8))) != 0:
                   explanation = "Trial " + `i` + " : baseline=" + `bvalue` + " result=" + `tvalue` + " (%.2f"%(round(tvalue / bvalue * 100.0, 2))  + "% of baseline)"
                elif round(abs(bvalue-tvalue),8) > 0:
                   explanation = "Trial " + `i` + " : baseline=" + `bvalue` + " result=" + `tvalue` + " (result differs from baseline)"
                if (self.sense == 0) and (abs(tvalue-bvalue) > tol):
                   explanation = "Trial " + `i` + " has absolute difference greater than " + `tol` + " : baseline=" + `bvalue` + " result=" + `tvalue`
                   if (bvalue != 0) and (tol > 0.0):
                       explanation = explanation + " (tolerance exceeded by %.2f"%(round(abs(tvalue-bvalue)/tol*100.0 - 100.0, 2))  + "%)"
                   status = "Fail"
                   break
                elif (self.sense != 0) and ((self.sense*(tvalue-bvalue)) > tol):
                   if self.sense > 0:
                      explanation = "Trial " + `i` + " has Result-Baseline greater than " + `tol` + " : baseline=" + `bvalue` + " result=" + `tvalue`
                      if (bvalue != 0):
                          explanation = explanation + " (increased %.2f"%(round(tvalue/bvalue*100.0, 2) - 100.0)  + "%)"
                   else:
                      explanation = "Trial " + `i` + " has Baseline-Result greater than " + `tol` + " : baseline=" + `bvalue` + " result=" + `tvalue`
                      if (bvalue != 0):
                          explanation = explanation + " (decreased %.2f"%(100.0 - round(tvalue/bvalue*100.0, 2))  + "%)"
                   status = "Fail"
                   break
             else:
                explanation = "Trial " + `i` + " unknown measurement type"
                status = "Fail"
                break
        return (explanation,status)

    def write_analysis_results(self,OUTPUT):
        for expname in self.results.keys():
          for combination in self.results[expname]:
            print >>OUTPUT, "   <Test experiment=\"" + expname + "\" id=\"" + combination.name + "\">"
            print >>OUTPUT, "     <Options>"
            print >>OUTPUT, "     " + combination.expparams.strip()
            print >>OUTPUT, "     </Options>"
            if self.test_status[expname][combination.name] == "Pass":
               print >>OUTPUT, "     <Status>Pass</Status>"
               if len(self.test_explanation[expname][combination.name]) > 0:
                   print >>OUTPUT, "     <Explanation>" + self.test_explanation[expname][combination.name] + "</Explanation>"
            else:
               print >>OUTPUT, "     <Status>Fail</Status>"
               print >>OUTPUT, "     <Explanation>" + self.test_explanation[expname][combination.name] + "</Explanation>"
            print >>OUTPUT, "   </Test>"

    def read_analysis_results(self,node):
        for cnode in node.childNodes:
          if cnode.nodeType == Node.ELEMENT_NODE:
             cnode_name = cnode.nodeName.lower()
             if cnode_name == "test":
                expname=""
                comb=""
                for (name,value) in cnode.attributes.items():
                  if name == "experiment":
                          expname=value
                     #XXX print " read: experiment=", expname   #syc
                  elif name == "id":
                     comb=value
                     #XXX print " read: comb=", comb   #syc
                if expname not in self.test_status.keys():
                   self.test_status[expname] = {}
                   self.test_explanation[expname] = {}
                for gnode in cnode.childNodes:
                  if gnode.nodeType == Node.ELEMENT_NODE:
                     gnode_name = gnode.nodeName.lower()
                     if gnode_name == "explanation":
                        value = get_xml_text(gnode)
                        self.test_explanation[expname][comb] = value
                     elif gnode_name == "status":
                        value = get_xml_text(gnode)
                        self.test_status[expname][comb] = (value == "Pass")


    def num_tests(self, status=None):
        num=0
        for tstatus in self.test_status.values():
            for value in tstatus.values():
              if status is None or value == status:
                 num=num+1
        return num

#
# The 'lcov' analysis processes auxillary files generated during an 
# experiment and generates HTML files to summarize coverage statistics.
#
class LCOVAnalysis(AnalysisBase):
    def __init__(self,node=None):
        """
        An object that can analyze the code coverage generated
        by an experiment.
        """
        self.source_root=None
        self.html_dir="lcov/html"
        self.lcov_dir="lcov"
        self.title=None
        self.keep_data=False
        AnalysisBase.__init__(self,node)


    def process_options(self, olist):
        """
        Process a list of option/value pairs
        """
        AnalysisBase.process_options(self,olist)
        if self.source_root is None:
           raise ValueError, "Undefined source root"
        if self.title is None:
           self.title="EXACT LCOV Analysis For " + self.source_root

    def execute(self, exps, print_summary=True, force=False, expstudy="unknown"):
        """
        Analyze an experiment.
        """
        self.process_options(["", self._options])
        if not os.path.exists(self.lcov_dir):
           os.system("mkdir " + self.lcov_dir)
        os.system("rm -Rf " + self.lcov_dir + "/*")
        if self.html_dir[0] != '/' and self.html_dir[0] != '~':
           self.html_dir = commands.getoutput("pwd") + "/" + self.html_dir
        if not os.path.exists(self.html_dir):
           os.system("mkdir " + self.html_dir)
        gcda_files = commands.getoutput("find " + self.source_root + " -name '*.gcda'")
        if gcda_files != "":
           filestr = commands.getoutput("echo \"" + gcda_files + "\" | grep -v 'packages/tpl' | xargs -n1      dirname | sort | uniq")
           #print "HERE X",filestr,"X"
           dirs = filestr.split(None)
           #print "HERE",dirs
           print ""
           print "LCOV is Processing the Following Directories"
           for dir in dirs:
             print " ",dir
             #print "lcov -d " + dir + " -c -f >> " + self.lcov_dir + "/final.info 2>> lcov.out"
             os.system("lcov -d " + dir + " -c -f >> " + self.lcov_dir + "/final.info 2>> " + self.lcov_dir + "/lcov.out")
           print "Generating HTML"
           os.system("(pwd; cd " + self.lcov_dir + " ; genhtml.pl -o " + self.html_dir + " -k final.info -t \'" + self.title + "\') 2>&1 > " + self.lcov_dir + "/genhtml.out")
        if not self.keep_data:
           os.system("find " + self.source_root + " -name '*.gcda' | xargs --no-run-if-empty /bin/rm")

#
# This class defines an analysis that writes out one or more 
# experiments to a single table that can be read into R/Splus.
#
class TableAnalysis(AnalysisBase):
    def __init__(self,node=None):
        """
        An object that can analyze an experiment to validate one
        or more values in the experiment.
        """
        self.test_status={}
        self.output_file=None
        self.solver="data"
        self.output_format="txt"
        self.record_option=[]
        self.columns=[]
        AnalysisBase.__init__(self,node)

    def num_tests(self, status=None):
        num=0
        for tstatus in self.test_status.values():
            for value in tstatus.values():
              if status is None or value == status:
                 num=num+1
        return num

    def process_options(self, olist):
        """
        Process a list of option/value pairs
        """
        AnalysisBase.process_options(self,olist)

    def initialize_callback(self, node):
        cnode_name = node.nodeName.lower()
        if cnode_name == "format":
           for (name,value) in node.attributes.items():
             if name.lower() == "type":
                self.output_format = str(value)
        elif cnode_name == "column":
           for (name,value) in node.attributes.items():
             if name.lower() == "measurement":
                self.columns.append( (name.lower(),str(value)) )
             elif name.lower() == "option":
                self.columns.append( (name.lower(),str(value)) )
                self.record_option.append(str(value));
           

    def execute(self, exps, print_summary=True, force=False, expstudy="unknown"):
        """
        Analyze an experiment.
        """
        self.process_options(["", self._options])
        if self.output_file is None:
           if self.output_format == "txt":
              self.output_file=self._name+"-table.txt"
           elif self.output_format == "csv":
              self.output_file=self._name+"-table.csv"
           elif self.output_format == "R":
              self.output_file=self._name+"-table.R"
        if len(self._data) == 0:
           raise ValueError, "Undefined experiment name(s)"
        j=1
        for i in self._data:
          if print_summary:
             print "      Analysis:   " + self._name + "." + i.experiment + " ",
          self.execute_analysis(exps[i.experiment].results, print_summary, i.experiment, i.filter, j, self.output_format)
          j=j+1

    def execute_analysis(self, res, print_summary, expname, filter, counter, format):
        #
        # Collect header line
        #
        factor_data={}
        factor_data["ExpID"] = []
        factor_data["TreatmentID"] = []
        for factor in res.factorNames():
          factor_data[factor] = []
        factor_names = ["ExpID", "TreatmentID"] + res.factorNames()
        #
        # Collect Factorial Info
        #
        option_data={}
        for val in self.record_option:
          option_data[val] = [ copy.copy(val) ]
        for combination in res:
          #
          # Ignore filtered combinations
          #
          if filter is not None and not filter.verify(combination):
             continue
          #
          # Process combination-specific options
          #
          self.process_options([combination.expparams, self._options])
          #
          # Ignore combinations with no results
          #
          if len(combination) == 0:
             continue
          #
          # Collect Combination ID
          #
          factor_data["ExpID"].append(str(counter))
          factor_data["TreatmentID"].append(combination.name)
          #
          # Collect combination attributes
          #
          i=0
          j=2
          for val in combination.tuple_key():
            if i % 2 == 0:
               #print combination.levelText(name)
               factor_data[ factor_names[j] ].append(combination.levelText(val))
               j=j+1
            #else:
               #name=val
            i=i+1
          missing_flag=False
          for val in self.record_option:
            if val not in self.option_dict.keys():
               #print "  Missing option ",val
               missing_flag=True
            if val in self.option_dict.keys():
               option_data[val].append( copy.copy(self.option_dict[val]) )
            else:
               option_data[val].append( "NA" )
          if global_data.debug and missing_flag:
             print "  Valid Options: ", self.option_dict.keys()
        #
        # Collect Measurement Info
        #
        data={}
        for combination in res:
          for trial in combination:
            for measurement in res.measurements():
               if measurement not in data.keys():
                  data[measurement] = []
               if not (measurement in trial.keys()):
                  data[measurement].append("NA")
               else:
                  if not isinstance(trial[measurement],Measurement):
                     data[measurement].append(str(trial[measurement]))
                  elif (trial[measurement].value == "ERROR") or \
                     (trial[measurement].value == ""):
                     data[measurement].append("NA")
                  elif trial[measurement].type == "text/string":
                     data[measurement].append(trial[measurement].value)
                  else:
                     data[measurement].append(str(trial[measurement].value))

        unknown_measurement=""
        self.table = []
        for col in self.columns:
          if col[0] == "measurement":
             self.table.append( [ col[1] ] )
             if col[1] in data.keys():
                self.table[-1] = self.table[-1] + data[col[1]]
             else:
                unknown_measurement=col[1]
                self.table[-1] = self.table[-1] + ["NA"]*len(self.table[0])
          elif col[0] == "option":
             #
             # BUG: this won't work with multiple trials
             #
             self.table.append( option_data[col[1]] )
        for name in factor_names:
          self.table.append( [name] );
          self.table[-1] = self.table[-1] + factor_data[name]
        if unknown_measurement != "":
           print ""
           print " Trying to Use an Unknown Measurement: " + unknown_measurement
           print " Experimental Measurements: ", data.keys()

        if format=="txt":
           OUTPUT=open(self.output_file,"w")
           for i in range(0,len(self.table[0])):
             for j in range(0,len(self.table)):
               if j > 0:
                  print >>OUTPUT, "\t",
               if i >= len(self.table[j]):
                  print >>OUTPUT, "NA",
               else:
                  if i == 0 or ' ' in self.table[j][i]:
                     print >>OUTPUT, "\""+self.table[j][i]+"\"",
                  else:
                     print >>OUTPUT, self.table[j][i],
             print >>OUTPUT, ""
           OUTPUT.close()
        elif format=="csv":
           OUTPUT=os.open(self.output_file,os.O_WRONLY|os.O_CREAT)
           for i in range(0,len(self.table[0])):
             for j in range(0,len(self.table)):
               if j > 0:
                  os.write(OUTPUT,",")
               if i >= len(self.table[j]):
                  os.write(OUTPUT,"NA")
               else:
                  os.write(OUTPUT,str(self.table[j][i]))
             os.write(OUTPUT,"\n")
           os.close(OUTPUT)
               
    def execute_analysis_R(self, res, print_summary, expname, filter, counter):
        OUTPUT=open(self.output_file,"w")
        #
        # Print header line
        #
        print >>OUTPUT, self.solver + " <- list()"
        print >>OUTPUT, "factor.names <- c('ExpID','TreatmentID'",
        for factor in res.factorNames():
          print >>OUTPUT, ",'"+factor+"'",
        print >>OUTPUT, ")"
        #
        # Print Factorial Info
        #
        print >>OUTPUT, "factor.data <- c("
        first=True
        for combination in res:
          #
          # Ignore filtered combinations
          #
          if filter is not None and not filter.verify(combination):
             continue
          #
          # Process combination-specific options
          #
          self.process_options([combination.expparams, self._options])
          #
          # Ignore combinations with no results
          #
          if len(combination) == 0:
             continue
          #
          # Print Combination ID
          #
          if first==False:
             print >>OUTPUT,",",
          else:
             first=False
          print >>OUTPUT, "'"+str(counter) + "','" + combination.name+"'",
          #
          # Print combination attributes
          #
          i=0
          for val in combination.tuple_key():
            if i % 2 == 1:
               print >>OUTPUT, ",'"+val+"'",
            i=i+1
          #
          # Print measurements
          #
          print >>OUTPUT,""
        print >>OUTPUT,")"
        print >>OUTPUT,self.solver+"$factors <- data.frame(t(array(factor.data, c(length(factor.names), length(factor.data)/length(factor.names)))))"
        print >>OUTPUT,"attr(" + self.solver + "$factors,\"names\") <- factor.names"
        #
        # Print Measurement Info
        #
        data={}
        for combination in res:
          for trial in combination:
            for measurement in res.measurements():
               if measurement not in data.keys():
                  data[measurement] = []
               if not (measurement in trial.keys()):
                  #print >>OUTPUT, " NA F",
                  data[measurement].append("NA")
               else:
                  if not isinstance(trial[measurement],Measurement):
                     #print >>OUTPUT, " "+str(trial[measurement])+" F",
                     data[measurement].append(str(trial[measurement]))
                  elif (trial[measurement].value == "ERROR") or \
                     (trial[measurement].value == ""):
                     #print >>OUTPUT, " NA F",
                     data[measurement].append("NA")
                  elif trial[measurement].type == "text/string":
                     #print >>OUTPUT, " \"" + trial[measurement].value + "\" T",
                     data[measurement].append(trial[measurement].value)
                  else:
                     #print >>OUTPUT, " " + str(trial[measurement].value) + " T",
                     data[measurement].append(str(trial[measurement].value))
          #print >>OUTPUT, ""
        for key in data.keys():
          print >>OUTPUT, self.solver+"$" + string.replace(key," ","_") + "<-c(",
          first=True
          for val in data[key]:
            if not first:
               print >>OUTPUT, ",",
            else:
               first=False
            print >>OUTPUT,"'"+val+"'",
          print >>OUTPUT,")"
        OUTPUT.close()

    def write_analysis_results(self,OUTPUT):
        raise IOError, "Table written to '" + self.output_file + "'"

#
# This class defines an analysis that writes out one or more 
# experiments to a single table that can be read into R/Splus.
#
class RTableAnalysis(AnalysisBase):
    def __init__(self,node=None):
        """
        An object that can analyze an experiment to validate one
        or more values in the experiment.
        """
        self.test_status={}
        self.output_file=None
        self.solver="data"
        AnalysisBase.__init__(self,node)

    def num_tests(self, status=None):
        num=0
        for tstatus in self.test_status.values():
            for value in tstatus.values():
              if status is None or value == status:
                 num=num+1
        return num

    def process_options(self, olist):
        """
        Process a list of option/value pairs
        """
        AnalysisBase.process_options(self,olist)

    def execute(self, exps, print_summary=True, force=False, expstudy="unknown"):
        """
        Analyze an experiment.
        """
        self.process_options(["", self._options])
        if self.output_file is None:
           self.output_file=self._name+"-table.R"
        if len(self._data) == 0:
           raise ValueError, "Undefined experiment name(s)"
        j=1
        for i in self._data:
          if print_summary:
             print "      Analysis:   " + self._name + "." + i.experiment + " ",
          self.execute_analysis(exps[i.experiment].results, print_summary, i.experiment, i.filter, j)
          j=j+1

    def execute_analysis(self, res, print_summary, expname, filter, counter):
        OUTPUT=open(self.output_file,"w")
        #
        # Print header line
        #
        print >>OUTPUT, self.solver + " <- list()"
        print >>OUTPUT, "factor.names <- c('ExpID','TreatmentID'",
        for factor in res.factorNames():
          print >>OUTPUT, ",'"+factor+"'",
        print >>OUTPUT, ")"
        #
        # Print Factorial Info
        #
        print >>OUTPUT, "factor.data <- c("
        first=True
        for combination in res:
          #
          # Ignore filtered combinations
          #
          if filter is not None and not filter.verify(combination):
             continue
          #
          # Process combination-specific options
          #
          self.process_options([combination.expparams, self._options])
          #
          # Ignore combinations with no results
          #
          if len(combination) == 0:
             continue
          #
          # Print Combination ID
          #
          if first==False:
             print >>OUTPUT,",",
          else:
             first=False
          print >>OUTPUT, "'"+str(counter) + "','" + combination.name+"'",
          #
          # Print combination attributes
          #
          i=0
          for val in combination.tuple_key():
            if i % 2 == 1:
               print >>OUTPUT, ",'"+val+"'",
            i=i+1
          #
          # Print measurements
          #
          print >>OUTPUT,""
        print >>OUTPUT,")"
        print >>OUTPUT,self.solver+"$factors <- data.frame(t(array(factor.data, c(length(factor.names), length(factor.data)/length(factor.names)))))"
        print >>OUTPUT,"attr(" + self.solver + "$factors,\"names\") <- factor.names"
        #
        # Print Measurement Info
        #
        data={}
        for combination in res:
          for trial in combination:
            for measurement in res.measurements():
               if measurement not in data.keys():
                  data[measurement] = []
               if not (measurement in trial.keys()):
                  #print >>OUTPUT, " NA F",
                  data[measurement].append("NA")
               else:
                  if not isinstance(trial[measurement],Measurement):
                     #print >>OUTPUT, " "+str(trial[measurement])+" F",
                     data[measurement].append(str(trial[measurement]))
                  elif (trial[measurement].value == "ERROR") or \
                     (trial[measurement].value == ""):
                     #print >>OUTPUT, " NA F",
                     data[measurement].append("NA")
                  elif trial[measurement].type == "text/string":
                     #print >>OUTPUT, " \"" + trial[measurement].value + "\" T",
                     data[measurement].append(trial[measurement].value)
                  else:
                     #print >>OUTPUT, " " + str(trial[measurement].value) + " T",
                     data[measurement].append(str(trial[measurement].value))
          #print >>OUTPUT, ""
        for key in data.keys():
          print >>OUTPUT, self.solver+"$" + string.replace(key," ","_") + "<-c(",
          first=True
          for val in data[key]:
            if not first:
               print >>OUTPUT, ",",
            else:
               first=False
            print >>OUTPUT,"'"+val+"'",
          print >>OUTPUT,")"
        OUTPUT.close()

    def write_analysis_results(self,OUTPUT):
        raise IOError, "R data written to '" + self.output_file + "'"


#
# A simple function to register analysis class
#
def register_analysis(name, object_constructor):
        global_data.analysis_factory.register(name,object_constructor)

##
## Register EXACT's analysis classes
##
register_analysis("validation",ValidationAnalysis)
register_analysis("relative_performance",RelativePerformanceAnalysis)
register_analysis("baseline",BaselineAnalysis)
register_analysis("lcov",LCOVAnalysis)
register_analysis("table",TableAnalysis)

