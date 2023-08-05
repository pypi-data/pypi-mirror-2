import sys
sys.path = sys.path + [ '../python' ]
from fast import exact


def validation_fn(self, vals, ttype):
    if sys.platform=="cygwin":
       return ("",True)
    return exact.validate_fn_default(self,vals,ttype)

def compare_fn(self, sense, newval, value, tol, cmp_operator):
    return exact.compare_fn_default(self,sense,newval,value,tol,cmp_operator)

#print "example13.py"
