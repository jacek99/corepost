'''
Created on 2011-10-11
@author: jacekf

Responsible for converting return values into cleanly serializable dict/tuples/lists
for JSON/XML/YAML output
'''

import inspect, collections
from jinja2 import Template
from UserDict import DictMixin

xmlListTemplate = Template("""<list>{% for item in items %}<item>{% for prop,val in item.iteritems() %}<{{prop}}>{{val}}</{{prop}}>{% endfor %}</item>{% endfor %}</list>""")
xmlTemplate = Template("""<item>{% for prop,val in item.iteritems() %}<{{prop}}>{{val}}</{{prop}}>{% endfor %}</item>""")

def convertForSerialization(obj):
    """Converts anything (clas,tuples,list) to the safe serializable equivalent"""
    if isinstance(obj, dict) or isinstance(obj,DictMixin):
        return traverseDict(obj)
    elif isClassInstance(obj):
        return convertClassToDict(obj)
    elif isinstance(obj,collections.Iterable):
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
        if inspect.isclass(val):
            # call itself recursively
            val = convertClassToDict(val)
        newDict[prop] = val
    
    return newDict
    
def generateXml(object):
    """Generates basic XML from an object that has already been converted for serialization"""
    if isinstance(object,dict):
        return str(xmlTemplate.render(item=object.keys()))
    elif isinstance(object,collections.Iterable):
        return str(xmlListTemplate.render(items=object))
    else:
        raise RuntimeError("Unable to convert to XML: %s" % object)    
    
def isClassInstance(object):
    """Checks if a given object is a class instance"""
    return getattr(object, "__class__",None) != None and not isinstance(object,dict) and not isinstance(object,tuple) and not isinstance(object,list)