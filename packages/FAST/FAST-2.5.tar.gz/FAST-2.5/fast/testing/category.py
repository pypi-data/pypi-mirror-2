#  _________________________________________________________________________
#
#  FAST: Python tools for software testing.
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the FAST README.txt file.
#  _________________________________________________________________________

from pyutilib.component.core import *

class ITestCategory(Interface):
    """An interface for services that define test categories"""
    
    def get_name(self):
        return self.name


class Category(Plugin):

    implements(ITestCategory)

    def __init__(self, name, members=[], default=None):
        self.name=name
        self.members=set(members)
        self.default=default

    def get_name(self):
        return self.name

    def __contains__(self, tag):
        return tag in self.members


def add_tag(category, tag, doc=None, default=False):
    """Add a tag"""
    #
    # Find the category with this name
    #
    categories = ExtensionPoint(ITestCategory)
    cat = None
    for item in categories:
        if item.get_name() == category:
            cat=item
            break
    #
    # Create the category if none exists
    #
    if cat is None:
        cat = Category(category)
    #
    # Populate this category
    #
    cat.members.add(tag)
    if default:
        cat.default = tag
