#  _________________________________________________________________________
#
#  FAST: Python tools for software testing.
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the FAST README.txt file.
#  _________________________________________________________________________

from fast import exact

class Build(exact.XMLObjectBase):
    def __init__(self, node=None):
	if node is not None:
	   self.initialize(node)

    def parse_xml(self,node):
	for cnode in node.childNodes:
	  if cnode.nodeType == Node.ELEMENT_NODE:
	     if cnode.nodeName.lower() == "executionstatus":
	        self.estat = str(get_text(cnode))
	     elif cnode.nodeName.lower() == "integritystatus":
	        self.istat = str(get_text(cnode))


class Configure(exact.XMLObjectBase):
    def __init__(self, node=None):
	if node is not None:
	   self.initialize(node)

    def parse_xml(self,node):
	pass


class CodeCheck(exact.XMLObjectBase):
    def __init__(self, node=None):
	if node is not None:
	   self.initialize(node)

    def parse_xml(self,node):
	pass


class Config(exact.XMLObjectBase):
    def __init__(self, node=None):
	if node is not None:
	   self.initialize(node)

    def parse_xml(self,node):
	pass


class FASTInterfaceObject(exact.GenericInterfaceObject):
    def __init__(self, webdir, filename):
        exact.GenericInterfaceObject.__init__(self,None)
	self.webdir=webdir
        self.initialize(filename)


    def reset(self):
        self.instance = None
        exact.GenericInterfaceObject.reset(self)


    def parse_xml(self, node):
        if exact.global_data.debug:
           print "Generic Node Name: " + node.nodeName
        node_name = node.nodeName.lower()
        if node_name == "build":
           self.instance = Build(node)
           self.instance.filename = self.filename
        elif node_name == "config":
           self.instance = Config(node,False)
           self.instance.filename = self.filename
        elif node_name == "codecheck":
           self.instance = CodeCheck(node)
           self.instance.filename = self.filename
        elif node_name == "configure":
           self.instance = Configure(node)
           self.instance.filename = self.filename
        else:
           exact.GenericInterfaceObject.parse_xml(self,node)
           self.instance.webdir = self.webdir


def FASTInterface(webdir,filename):
  object = FASTInterfaceObject(webdir,filename)
  return object.instance
