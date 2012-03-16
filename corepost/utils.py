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

def checkExpectedInterfaces(objects,expectedInterface):
    """Verifies that all the objects implement the expected interface"""
    for obj in objects:
        if not expectedInterface.providedBy(obj):
            raise RuntimeError("Object %s does not implement %s interface" % (obj,expectedInterface))

def safeDictUpdate(dictObject,key,value):
    """Only adds a key to a dictionary. If key exists, it leaves it untouched"""
    if key not in dictObject:
        dictObject[key] = value
        