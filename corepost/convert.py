'''
Created on 2011-10-11
@author: jacekf

Responsible for converting return values into cleanly serializable dict/tuples/lists
for JSON/XML/YAML output
'''

import collections
from UserDict import DictMixin

primitives = (int, long, float, bool, str,unicode)

def convertForSerialization(obj):
    """Converts anything (clas,tuples,list) to the safe serializable equivalent"""
    if type(obj) in primitives:
        # no conversion
        return obj 
    elif isinstance(obj, dict) or isinstance(obj,DictMixin):
        return traverseDict(obj)
    elif isClassInstance(obj):
        return convertClassToDict(obj)
    elif isinstance(obj,collections.Iterable) and not isinstance(obj,str):
        # iterable
        values = []
        for val in obj:
            values.append(convertForSerialization(val))
        return values
    else:
        # return as-is
        return obj

def convertClassToDict(clazz):
    """Converts a class to a dictionary"""
    properties = {}
    for prop,val in clazz.__dict__.iteritems():
        #omit private fields
        if not prop.startswith("_"):
            properties[prop] = val

    return traverseDict(properties)

def traverseDict(dictObject):
    """Traverses a dict recursively to convertForSerialization any nested classes"""
    newDict = {}

    for prop,val in dictObject.iteritems():
        newDict[prop] = convertForSerialization(val)
    
    return newDict
    
def generateXml(obj):
    """Generates basic XML from an object that has already been converted for serialization"""
    if isinstance(obj, dict) or isinstance(obj,DictMixin):
        return getXML_dict(obj, "item")
    elif isinstance(obj,collections.Iterable):
        return "<list>%s</list>" % getXML(obj, "item")
    else:
        raise RuntimeError("Unable to convert to XML: %s" % obj)    
    
def isClassInstance(obj):
    """Checks if a given obj is a class instance"""
    return getattr(obj, "__class__",None) != None and not isinstance(obj,dict) and not isinstance(obj,tuple) and not isinstance(obj,list) and not isinstance(obj,str)

## {{{ http://code.activestate.com/recipes/440595/ (r2)
def getXML(obj, objname=None):
    """getXML(obj, objname=None)
    returns an object as XML where Python object names are the tags.
    
    >>> u={'UserID':10,'Name':'Mark','Group':['Admin','Webmaster']}
    >>> getXML(u,'User')
    '<User><UserID>10</UserID><Name>Mark</Name><Group>Admin</Group><Group>Webmaster</Group></User>'
    """
    if obj == None:
        return ""
    if not objname:
        objname = "item"
    adapt={
        dict: getXML_dict,
        list: getXML_list,
        tuple: getXML_list,
        }
    if adapt.has_key(obj.__class__):
        return adapt[obj.__class__](obj, objname)
    else:
        return "<%(n)s>%(o)s</%(n)s>"%{'n':objname,'o':str(obj)}

def getXML_dict(indict, objname=None):
    h = "<%s>"%objname
    for k, v in indict.items():
        h += getXML(v, k)
    h += "</%s>"%objname
    return h

def getXML_list(inlist, objname=None):
    h = ""
    for i in inlist:
        h += getXML(i, objname)
    return h
## end of http://code.activestate.com/recipes/440595/ }}}

