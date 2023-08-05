#  _________________________________________________________________________
#
#  FAST: Python tools for software testing.
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the FAST README.txt file.
#  _________________________________________________________________________

import category
from pyutilib.component.core import *
import logging
import os
import re

PluginGlobals.push_env("fast.testing")


class Test(object):

    def __init__(self, data, tester):
        self.data=data
        self.tester=tester

    def run(self):
        """Run the tester on this data"""
        self.artifacts = self.tester.run(self.data)
        return self.artifacts


class ITester(Interface):
    """A class that defines the actions of a tester"""

    def match_type(self, type):
        """Returns true if this is the right type of tester"""

    def match_tags(self, tags):
        """Returns true if this tester matches the requirements for the test tags."""

    def generate(self, identifiers, option):
        """Return a list of Test objects, given configuration options"""


class BaseTester(Plugin):

    implements(ITester)

    categories = ExtensionPoint(category.ITestCategory)

    def __init__(self, package=None, type=type, tags=[], dir=None):
        self.package=package
        self.type=type
        self.dir=dir
        #
        # Define a dictionary that summarizes the test
        # categorization that are required for this tester.
        #
        self.descr = {}
        for cat in BaseTester.categories:
            cname = cat.get_name()
            self.descr[cname] = None
            for tag in tags:
                if tag in cat:
                    self.descr[cname] = tag
                    break
        self.log = logging.getLogger("fast.testing")

    def match_type(self, type):
        #
        # If the type is a string, test it
        #
        if isinstance(type,basestring):
            return self.type == type
        #
        # If type is an empty list, then return True
        #
        if len(type) == 0:
            return True
        for i in type:
            if self.type == i:
                return True
        return False

    def match_tags(self, tags):
        for tag in tags:
            tag_matches=False
            for cat in BaseTester.categories:
                cname = cat.get_name()
                if tag in cat:
                    if not self.descr[cname] is None and tag != self.descr[cname]:
                        self.log.debug("BaseTester:match_tags returns False because the tag %s is specified, but tester %s requires value %s for category %s" % (tag, self.name, self.descr[cname], cname))
                    else:
                        tag_matches=True
            if not tag_matches:
                self.log.debug("BaseTester:match_tags returns False because the tag %s is specified, this does not match any category" % (tag))
                return False
        return True

    def list_matching_dirs(self, rootPath, regex):
        #
        # Q: should this use glob?
        # Q: should this only match directories?
        #
        if os.path.exists(regex):
            #
            # Normalize path names, and then test if
            # the regex is a directory that starts with the root
            # path.  If so, then we can simply return
            # the regex path.
            #
            root = os.path.abspath(rootPath.lower())
            curr = os.path.abspath(regex.lower())
            if curr.startswith(root):
                return [regex]
        ans = []
        p = re.compile(regex)
        for root, dirs, files in os.walk(rootPath):
            for dir in dirs:
                if p.match(dir):
                    ans.append(dir)
        return ans


PluginGlobals.pop_env()
