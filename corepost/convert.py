'''
Created on 2011-10-11
@author: jacekf

Responsible for converting return values into cleanly serializable dict/tuples/lists
for JSON/XML/YAML output
'''

import collections
from jinja2 import Template
from UserDict import DictMixin

xmlListTemplate = Template("""<list>{% for item in items %}<item>{% for prop,val in item.iteritems() %}<{{prop}}>{{val}}</{{prop}}>{% endfor %}</item>{% endfor %}</list>""")
xmlTemplate = Template("""<item>{% for prop,val in item.iteritems() %}<{{prop}}>{{val}}</{{prop}}>{% endfor %}</item>""")

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
    if isinstance(object,dict):
        return str(xmlTemplate.render(item=obj.keys()))
    elif isinstance(obj,collections.Iterable):
        return str(xmlListTemplate.render(items=obj))
    else:
        raise RuntimeError("Unable to convert to XML: %s" % obj)    
    
def isClassInstance(obj):
    """Checks if a given obj is a class instance"""
    return getattr(obj, "__class__",None) != None and not isinstance(obj,dict) and not isinstance(obj,tuple) and not isinstance(obj,list) and not isinstance(obj,str)
