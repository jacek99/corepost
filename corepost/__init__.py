'''
Common classes
'''

from zope.interface import Interface, Attribute

#########################################################
#
# INTERFACES
#
#########################################################

class IRESTResource(Interface):
    """An interface for all REST services that can be added within a root CorePost resource"""
    services = Attribute("All the REST services contained in this resource")


#########################################################
#
# CLASSES
#
#########################################################

class Response:
    """
    Custom response object, can be returned instead of raw string response
    """
    def __init__(self,code=200,entity=None,headers={}):
        self.code = code
        self.entity=entity if entity != None else ""
        self.headers=headers  
        
    def __str__(self):
        return str(self.__dict__)
    
class RESTException(Exception):
    """Standard REST exception that gets converted to the Response it passes in"""    
    def __init__(self, response):
        self.response = response
        
class NotFoundException(RESTException):
    """Standard 404 exception when REST resource is not found"""    
    def __init__(self, resourceName, invalidValue):
        RESTException.__init__(self,Response(404,"Unable to find %s identified by '%s'" % (resourceName,invalidValue), {"x-corepost-resource":resourceName,"x-corepost-value":invalidValue}))
        
class ConflictException(RESTException):
    """Standard 409 exception when REST resource is not found. Allows to pass in a custom message with more details"""    
    def __init__(self, resourceName, invalidValue, message):
        RESTException.__init__(self,Response(409,"Conflict for %s identified by '%s': %s" % (resourceName,invalidValue, message), {"x-corepost-resource":resourceName,"x-corepost-value":invalidValue}))
        
class AlreadyExistsException(ConflictException):
    """Standard 409 exception when REST resource already exists during a POST"""    
    def __init__(self, resourceName, invalidValue, message = None):
        ConflictException.__init__(self, resourceName, invalidValue, "%s already exists" % resourceName)

class InternalServerException(RESTException):
    """Standard 500 error"""    
    def __init__(self, safeErrorMessage):
        RESTException.__init__(self,Response(500,safeErrorMessage))
