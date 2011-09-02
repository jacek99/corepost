'''
Various CorePost utilities
'''
from inspect import getargspec

def getMandatoryArgumentNames(f):
    '''Returns a tuple of the mandatory arguments required in a function'''
    args,_,_,defaults = getargspec(f)
    if defaults == None:
        return args
    else:
        return args[0:len(args) - len(defaults)]
    