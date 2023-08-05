#  _________________________________________________________________________
#
#  FAST: Python tools for software testing.
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the FAST README.txt file.
#  _________________________________________________________________________

import os
import types
import re
from exact_xml import *
from misc_utilities import *
from exact_globals import *
from experiment import *
from analysis import *
from pyutilib.misc import get_xml_text, recursive_delete


class ExperimentalStudy(XMLObjectBase):
    def __init__(self, node=None, load_results=True, path=None, only_results=False, key=None):
        """
An experimental study object, which contains one or more 
experiments and experimental analyses.

Note: this object could be initialize with a node from an XML tree,
or with a filename, or with no argument at all

Note: when an experimental study is created, results are loaded 
if they are found.  Otherwise, an explicit 'readResults()' needs to
be called when results are generated after this object is constructed.
"""
        XMLObjectBase.__init__(self)
        self.autoload=load_results
        self.only_results=only_results
        self.reset()
        self.true_path=path
        self.key=key
        if node:
           self.initialize(node,False)


    def reset(self):
        self.name = "study"
        self.experiments = {}
        self.experiment_keys = []
        self.analyses = {}
        self.analysis_keys = []
        self.tags = set()
        XMLObjectBase.reset(self)


    def parse_xml(self, node):
        """
        Initialize the study with a node of an XML parsed tree.
        """
        #
        #
        #
        tmp = os.path.basename(self.filename).split('#')
        if len(tmp) > 1:
           self.prefix="#".join(tmp[:-1])+"#"
        else:
           self.prefix=""
        #
        # Load in from an XML node
        #
        for (name,value) in node.attributes.items():
          if name == "name":
             self.name = str(value)
        self.path = self.true_path
        for cnode in node.childNodes:
          if cnode.nodeType == Node.ELEMENT_NODE:
             if cnode.nodeName.lower() == "path":
                self.path = str(get_xml_text(cnode))
                self.path = self.path.strip()
        if self.path is None:
           self.path = "./" + self.name
        for cnode in node.childNodes:
          if cnode.nodeType == Node.ELEMENT_NODE:
             if cnode.nodeName.lower() == "experiment":
                  exp = Experiment(cnode, len(self.experiments)+1, self.name, self.autoload, self.path, only_results=self.only_results)
                  self.experiments[exp.name] = exp
                  self.experiment_keys.append(exp.name)
             elif cnode.nodeName.lower() == "analysis":
                  analysis = Analysis(cnode, self.path, only_results=self.only_results,study=self.name,key=self.key)
                  try:
                     if self.autoload:
                        analysis.readResults(self.prefix + self.name)
                  except IOError, msg:
                     print "WARNING:", msg
                  self.analyses[analysis._name] = analysis
                  self.analysis_keys.append(analysis._name)
             elif cnode.nodeName.lower() == "tags":
                  for gnode in cnode.childNodes:
                    if gnode.nodeType == Node.ELEMENT_NODE and\
                       gnode.nodeName.lower() == "tag":
                       self.tags = self.tags.union(set([get_xml_text(gnode)]))


    def clean(self,deleteRoot=True):
      recursive_delete(self.path,deleteRoot)


    def readResults(self, filename=None):
        """
        Read results from an XML file.
        If no filename is given, then try to read from the default path.
        """
        if filename is None:
           for exp in self.experiments:
             try: 
                exp.readResults(studyname=self.name)
                #exp.readResults(self.path,self.name)
             except IOError:
                dummy=1 
        else:
           #
           # TODO - interrogate the XML file to get the experiment name.
           # This will be more robust.
           #
           # syc: this gets the exp name from the filename, NOT the results inside!
           expname = filename.split('.')[-3]
           try:
             self.experiments[expname].readResults(filename=filename)
           except IOError:
             dummy=1 
           except KeyError:
             print "EXPNAME =", expname, " (experiment name not derived from filename, must be in name.expname.results.xml format)"
             raise


    def execute(self,taglist,factors,force=True,experiment_name=".*",analysis_name=".*"):
        #
        # Perform execution if the taglist is empty, or if
        # there is a matching tag in the study's set of tags
        #
        if len(taglist) == 0 or len(self.tags.intersection(set(taglist))) > 0:
           if global_data.debug:
              print "Experimental study " + self.name + " data will be put in directory " + self.path
           if not os.path.exists(self.path):
              os.mkdir(self.path)
           if global_data.debug:
              print "Executing study with tags: " + `taglist`
           if experiment_name is not None:
              p = re.compile(experiment_name)
              for key in self.experiment_keys:
                if p.match(key) is not None:
                   self.experiments[key].execute(factors,self.filename,force=force)
           if analysis_name is not None:
              imports = {}
              p = re.compile(analysis_name)
              for key in self.analysis_keys:
                if p.match(key) is None:
                   continue
                try:
                  if global_data.debug:
                     print "Executing analysis " + key
                  tmp = {}
                  for exp in self.analyses[key]._data:
                    if not exp.expimport:
                         #print "HERE",exp.experiment
                       if exp.experiment not in self.experiments.keys():
                          print ""
                          print "ERROR: undefined experiment \"" + exp.experiment + "\" in study \"" + self.name + "\""
                          sys.exit(1)
                       tmp[exp.experiment] = self.experiments[exp.experiment]
                       #print "HERE",tmp[exp.experiment].results,self.experiments[exp.experiment].path
                       #print "HERE",len(tmp[exp.experiment].results)
                       #if len(tmp[exp.experiment].results) == 0:
                       #   exp.expimport = exp.experiment
                    else:
                       #
                       # TODO external import - assume its a file right now
                       #
                       if exp.results_file:
                          #
                          # Do not try to load in data, but explicitly load in the results file.
                          #
                          import_obj = GenericInterface(exp.expimport,False)
                          import_obj.readResults(exp.results_file)
                       else:
                          #
                          # Assume that an experimental directory exists that we can read from
                          #
                          import_obj = GenericInterface(exp.expimport,True)
                       if isinstance(import_obj,ExperimentalStudy):
                          if exp.experiment not in import_obj.experiments.keys():
                             raise LookupError, "ERROR: Unknown experiment " + exp.experiment + " in study " + import_obj.name
                          tmp[exp.experiment] = import_obj.experiments[exp.experiment]
                          if len(tmp[exp.experiment].results) == 0:
                             raise ValueError, "ERROR: Experiment \"" + exp.experiment + "\" in study \"" + import_obj.name + "\" does not contain experimental results"
                       elif isinstance(import_obj,Experiment):
                          tmp[exp.experiment] = import_obj
                       else:
                          raise IOError, "ERROR: read in a bad type of XML object from file " + exp.expimport
                     
                       imports[(exp.expimport,exp.experiment)] = import_obj
                    tmp[exp.experiment].filter = exp.filter
                  self.analyses[key].execute(tmp, force=force, expstudy=self.name)
                  self.analyses[key].write_xml(self.name, force=force)
                except IOError, info:
                  print info
        else:
           if global_data.debug:
              print "Not executing study: no tags in list: " + `taglist`
        return


    def pprint(self,prefix=""):
        """
        Print out the information in the experimental study.
        """
        print prefix+"Experimental Study: " + self.name
        print prefix+"  Experiments: " + `len(self.experiments)`
        print prefix+"  Analyses:    " + `len(self.analyses)`
        print ""
        for name in self.experiment_keys:
          print prefix+"Experiment: " + name
          self.experiments[name].pprint(prefix+"  ")
          print ""
        for name in self.analysis_keys:
          print prefix+"Analysis:   " + name
          self.analyses[name].pprint(prefix+"  ")



class ScenarioKey(XMLObjectBase):
    def __init__(self, node=None):
        """
        Host information
        """
        XMLObjectBase.__init__(self)
        if node:
           self.initialize(node)


    def reset(self):
        self.kernel_name = None
        self.hostname = None
        self.kernel_release = None
        self.kernel_version = None
        self.machine = None
        self.processor = None
        self.os = None
        self.scenario = ""
        self.date = None


    def parse_xml(self, node):
        """
        Initialize the config info with a node of an XML parsed tree.
        """
        for (name,value) in node.attributes.items():
          if name == "KernelName":
             self.kernel_name = str(value)
          elif name == "HostName":
             self.hostname = str(value)
          elif name == "KernelRelease":
             self.kernel_release = str(value)
          elif name == "KernelVersion":
             self.kernel_version = str(value)
          elif name == "Machine":
             self.machine = str(value)
          elif name == "Processor":
             self.processor = str(value)
          elif name == "OS":
             self.os = str(value)
          elif name == "Scenario":
             self.scenario = str(value)
          elif name == "Date":
             self.date = str(value)
          

    def pprint(self, prefix=""):
        print prefix+ self.hostname + "/" + self.scenario


class SoftwareInfo(XMLObjectBase):
    def __init__(self, node=None):
        """
        Read in information from an XML configuration summary.
        """
        XMLObjectBase.__init__(self)
        if node:
           self.initialize(node)


    def reset(self):
        self.path = ""
        self.filename = ""
        self.key = None
        self.flags = ""
        self.log_file = ""
        self.start_time = ""
        self.run_time = ""
        self.execution_status = "Fail"
        self.integrity_status = "Fail"
        self.warnings = []
        self.build_info = None
        self.config_info = None
        XMLObjectBase.reset(self)


    def parse_xml(self, node):
        """
        Initialize the config info with a node of an XML parsed tree.
        """
        #
        # Load in from an XML node
        #
        for cnode in node.childNodes:
          if cnode.nodeType == Node.ELEMENT_NODE:
             cnode_name = cnode.nodeName.lower()
             if cnode_name == "key":
                 self.key = ScenarioKey(cnode)
             elif cnode_name == "flags":
                self.config_flags = get_xml_text(cnode)
             elif cnode_name == "logfile":
                self.log_file = get_xml_text(cnode)
             elif cnode_name == "starttime":
                self.start_time = get_xml_text(cnode)
             elif cnode_name == "runtime":
                self.run_time = get_xml_text(cnode)
             elif cnode_name == "executionstatus":
                self.execution_status = get_xml_text(cnode)
             elif cnode_name == "integritystatus":
                self.integrity_status = get_xml_text(cnode)
             elif cnode_name == "warnings":
                for gchild in cnode.childNodes:
                  if gchild.nodeType == Node.ELEMENT_NODE and\
                     gchild.nodeName.lower() == "explanation":
                     for (name,value) in gchild.attributes.items():
                       if name == "line":
                          self.warnings = self.warnings + [eval(value)]

        
    def pprint(self,prefix=""):
        print prefix+"Software Info: " + self.filename
        print prefix+"  Flags:           " + self.flags
        print prefix+"  LogFile:         " + self.log_file
        print prefix+"  StartTime:       " + self.start_time
        print prefix+"  RunTime:         " + self.run_time
        print prefix+"  ExecutionStatus: " + self.execution_status
        print prefix+"  IntegrityStatus: " + self.integrity_status
        print prefix+"  Warnings:        " + `len(self.warnings)`
        print prefix+"  Key:"
        if self.key:
           self.key.pprint(prefix+"  ")



class Scenario(XMLObjectBase):
    def __init__(self, node=None, path=None):
        """
        Read in information from an XML EXACT scenario summary.
        """
        XMLObjectBase.__init__(self)
        self.reset()
        self.path=path
        if node:
           self.initialize(node,False)


    def reset(self):
        self.path = ""
        self.filename = None
        self.key = None
        self.description = ""
        self.start_time = ""
        self.end_time = ""
        self.run_time = ""
        self.config_info = None
        self.build_info = None
        self.studies = {}
        self.files = []
        XMLObjectBase.reset(self)


    def parse_xml(self, node):
        """
        Initialize the scenario with a node of an XML parsed tree.
        """
        #
        # Load in from an XML node
        #
        for cnode in node.childNodes:
           if cnode.nodeType == Node.ELEMENT_NODE:
             cnode_name = cnode.nodeName.lower()
             if cnode_name == "key":
                 self.key = ScenarioKey(cnode)
             elif cnode_name == "description":
                self.description = get_xml_text(cnode)
             elif cnode_name == "starttime":
                self.start_time = get_xml_text(cnode)
             elif cnode_name == "endtime":
                self.end_time = get_xml_text(cnode)
             elif cnode_name == "runtime":
                self.run_time = get_xml_text(cnode)
             elif cnode_name == "files":
                ctr=1
                for gchild in cnode.childNodes:
                  if gchild.nodeType == Node.ELEMENT_NODE and\
                        gchild.nodeName.lower() == "name":
                        filename = get_xml_text(gchild)
                        self.files.append(filename)
                        if filename[-9:] == "build.xml":
                           self.build_info = SoftwareInfo(self.path + filename)
                        elif filename[-10:] == "config.xml":
                           self.config_info = SoftwareInfo(self.path + filename)
                        elif filename[-9:] == "study.xml":
                           self.studies["study_" + `ctr`] = ExperimentalStudy(self.path + filename, path=self.path, only_results=True, key=self.key)
                           ctr = ctr + 1

        
    def pprint(self,prefix=""):
        print "Scenario:"
        if self.config_info:
           self.config_info.pprint(prefix+"  ")
        if self.build_info:
           self.build_info.pprint(prefix+"  ")
        for key in self.studies.keys():
          print "  Experimental Study: " + key
          #syc: next line giving errors?
          self.studies[key].pprint(prefix+"    ")




class GenericInterfaceObject(XMLObjectBase):
    def __init__(self, filename, load_results=False):
        XMLObjectBase.__init__(self)
        self.load_results = load_results
        self.initialize(filename)
  

    def reset(self):
        self.instance = None
        XMLObjectBase.reset(self)


    def parse_xml(self, node):
        if global_data.debug:
           print "Generic Node Name: " + node.nodeName
        node_name = node.nodeName.lower()
        if node_name == "experimentalstudy" or node_name == "experimental-study": 
           self.instance = ExperimentalStudy(node,self.load_results)
           self.instance.filename = self.filename
        elif node_name == "experiment":
           self.instance = Experimental(node,False)
           self.instance.filename = self.filename
        elif node_name == "analysis":
           self.instance = Analysis(node)
           self.instance.filename = self.filename
        elif node_name == "scenario" or node_name == "testscenario":
           self.instance = Scenario(node,path=self.path)
           self.instance.filename = self.filename
        

def GenericInterface(filename, load_results=False):
  object = GenericInterfaceObject(filename,load_results)
  return object.instance


