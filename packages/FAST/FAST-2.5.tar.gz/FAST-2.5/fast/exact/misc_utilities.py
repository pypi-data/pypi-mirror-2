#  _________________________________________________________________________
#
#  FAST: Python tools for software testing.
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the FAST README.txt file.
#  _________________________________________________________________________


def flatten_dict(mydict):
    """
    A function that takes a dictionary and flattens it into a tuple in
    a uniform manner: keys are sorted, and the tuple consists of
    key-value pairs in order.
    """
    keys = mydict.keys()
    keys.sort()
    ans = ()
    for key in keys:
      ans += (key,)
      ans += (mydict[key],)
    return ans
