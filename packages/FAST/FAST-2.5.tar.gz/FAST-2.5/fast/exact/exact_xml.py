#  _________________________________________________________________________
#
#  FAST: Python tools for software testing.
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the FAST README.txt file.
#  _________________________________________________________________________


#import re
#import math
import os
import types
import sys
from xml.dom import minidom, Node
from exact_globals import *
import xml


class XMLObjectBase(object):
    def __init__(self):
        self.path=None


    def reset(self):
        self.filename = "unknown"


    def initialize(self, node, performReset=True):
        """
        Initialize the object with either a filename or a node of an 
        XML parsed tree.
        """
        if global_data.debug:
           print "XMLObjectBase::initialize",
           if isinstance(node,types.StringType) or isinstance(node,types.UnicodeType):
              print node
           if self.path is not None:
              print "Path " + self.path

        if performReset:
           self.reset()
        
        if node is None:
           return

        elif isinstance(node,types.StringType) or isinstance(node,types.UnicodeType):
           #
           # Load in from a file
           #
           if self.path is not None and self.path != "":
              self.filename = self.path + "/" + node
           else:
              self.filename = node

           if not os.path.exists(self.filename):
              print ""
              print "ERROR: missing file \"" + node + "\" when reading XML object"
              sys.exit(1)
           self.path = os.path.dirname(node)
           if self.path == "":
              self.path = "./"
           else:
              self.path = self.path + "/"
           #
           # Parse XML
           #
           try:
              doc = minidom.parse(self.filename)
           except xml.parsers.expat.ExpatError, e:
              print "ERROR: problem parsing XML file " + self.filename
              print e
              raise
           except:
              print "ERROR: problem parsing XML file " + self.filename
              raise
           #
           # Recursively call initialization, setting the current working
           # directory to the directory where the config-info file is
           # located.
           #
           try:
              #currdir = os.path.abspath('')
              #os.chdir(self.path)
              self.parse_xml(doc.documentElement)
           except:
              print "ERROR: problem initializing with data from the XML file " + self.filename
              #os.chdir(currdir)
              raise
           #os.chdir(currdir)
        else:
           self.parse_xml(node)

