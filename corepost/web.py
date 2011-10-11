'''
Main server classes

@author: jacekf
'''
from collections import defaultdict
from corepost import Response
from corepost.enums import Http, HttpHeader
from corepost.utils import getMandatoryArgumentNames, convertToJson
from corepost.routing import UrlRouter, CachedUrl, RequestRouter
from enums import MediaType
from formencode import FancyValidator, Invalid
from twisted.internet import reactor, defer
from twisted.web.http import parse_qs
from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET
import re, copy, exceptions, json, yaml
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from twisted.internet.defer import Deferred
    
class CorePost(Resource):
    '''
    Main resource responsible for routing REST requests to the implementing methods
    '''
    isLeaf = True
    
    def __init__(self,schema=None):
        '''
        Constructor
        '''
        self.__router = RequestRouter(self,schema)
        Resource.__init__(self)

    def render_GET(self,request):
        """ Handles all GET requests """
        return self.__renderUrl(request)
    
    def render_POST(self,request):
        """ Handles all POST requests"""
        return self.__renderUrl(request)
    
    def render_PUT(self,request):
        """ Handles all PUT requests"""
        return self.__renderUrl(request)
    
    def render_DELETE(self,request):
        """ Handles all DELETE requests"""
        return self.__renderUrl(request)
    
    def __renderUrl(self,request):
        try:
            val = self.__router.getResponse(request)
            
            # return can be Deferred or Response
            if isinstance(val,Deferred):
                val.addCallback(self.__finishRequest,request)
                return NOT_DONE_YET
            elif isinstance(val,Response):
                self.__applyResponse(request, val.code, val.headers)
                return val.entity
            else:
                raise RuntimeError("Unexpected return type from request router %s" % val)
        except Exception as ex:
            self.__applyResponse(request, 500, None)
            return str(ex)
        
    def __finishRequest(self,response,request):
        if not request.finished:
            self.__applyResponse(request, response.code,response.headers)
            request.write(response.entity)
            request.finish()
        
    def __applyResponse(self,request,code,headers={"content-type":MediaType.TEXT_PLAIN}):
        request.setResponseCode(code)
        if headers != None:
            for header,value in headers.iteritems():
                request.setHeader(header, value)
                
    def run(self,port=8080):
        """Shortcut for running app within Twisted reactor"""
        factory = Site(self)
        reactor.listenTCP(port, factory)    #@UndefinedVariable
        reactor.run()                       #@UndefinedVariable
       

##################################################################################################
#
# DECORATORS
#
##################################################################################################    

def route(url,methods=(Http.GET,),accepts=MediaType.WILDCARD,produces=None,cache=True):
    '''
    Main decorator for registering REST functions
    '''
    def decorator(f):
        def wrap(*args,**kwargs):
            return f
        router = UrlRouter(f, url, methods, accepts, produces, cache)
        setattr(wrap,'corepostRequestRouter',router)
        
        return wrap
    return decorator
    
def validate(schema=None,**vKwargs):
    '''
    Main decorator for registering additional validators for incoming URL arguments
    '''
    def fn(realfn):  
        def wrap(*args,**kwargs):
            # first run schema validation, then the custom validators
            errors = []
            if schema != None:
                try:
                    schema.to_python(kwargs)
                except Invalid as ex:
                    for arg, error in ex.error_dict.items():
                        errors.append("%s: %s ('%s')" % (arg,error.msg,error.value))
             
            # custom validators    
            for arg in vKwargs.keys():
                validator = vKwargs[arg]
                if arg in kwargs:
                    val = kwargs[arg]
                    try:
                        validator.to_python(val)
                    except Invalid as ex:
                        errors.append("%s: %s ('%s')" % (arg,ex,val))
                else:
                    if isinstance(validator,FancyValidator) and validator.not_empty:
                        raise TypeError("Missing mandatory argument '%s'" % arg)
            
            # fire error if anything failed validation
            if len(errors) > 0:
                raise TypeError('\n'.join(errors))
            # all OK
            return realfn(*args,**kwargs)
        return wrap
    return fn    
