'''
Various CorePost utilities
'''
from inspect import getargspec
import json
from corepost.enums import MediaType

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
    
def applyResponse(self,request,code,headers={"content-type":MediaType.TEXT_PLAIN}):
    """Applies response to current request"""
    request.setResponseCode(code)
    if headers != None:
        for header,value in headers.iteritems():
            request.setHeader(header, value)
