'''
Various CorePost utilities
'''
from inspect import getargspec
import json

def getMandatoryArgumentNames(f):
    '''Returns a tuple of the mandatory arguments required in a function'''
    args,_,_,defaults = getargspec(f)
    if defaults == None:
        return args
    else:
        return args[0:len(args) - len(defaults)]
    
def getRouterKey(method,url):
    '''Returns the common key used to represent a function that a request can be routed to'''
    return "%s %s" % (method,url)

def convertToJson(obj):
    """Converts to JSON, including Python classes that are not JSON serializable by default"""
    try:
        return json.dumps(obj)
    except Exception as ex:
        raise RuntimeError(str(ex))
