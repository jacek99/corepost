'''
Created on 2011-08-23

@author: jacekf
'''
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site
from collections import defaultdict

class Http:
    """Enumerates HTTP methods"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

class MediaType:
    """Enumerates media types"""    
    WILDCARD = "*/*"
    APPLICATION_XML = "application/xml"
    APPLICATION_ATOM_XML = "application/atom+xml"
    APPLICATION_XHTML_XML = "application/xhtml+xml"
    APPLICATION_SVG_XML = "application/svg+xml"
    APPLICATION_JSON = "application/json"
    APPLICATION_FORM_URLENCODED = "application/x-www-form-urlencoded"
    MULTIPART_FORM_DATA = "multipart/form-data"
    APPLICATION_OCTET_STREAM = "application/octet-stream"
    TEXT_PLAIN = "text/plain"
    TEXT_XML = "text/xml"
    TEXT_HTML = "text/html"
    
class RequestRouter:
    """ Common class for containing info related to routing a request to a function """
    def __init__(self,url,method,accepts,produces):
        self.__url = url
        self.__method = method
        self.__accepts = accepts
        self.__produces = produces
        
        #parse URL into regex used for matching
    
class CorePost(Resource):
    '''
    Main resource responsible for routing REST requests to the implementing methods
    '''
    isLeaf = True
    
    def __init__(self):
        '''
        Constructor
        '''
        self.__urls = defaultdict(dict)
        self.__cachedUrls = defaultdict(dict) # used to avoid routing request to function on every request
        self.__methods = {}

    def __registerFunction(self,f,url,methods,accepts,produces):
        if f not in self.__methods.values():
            if not isinstance(methods,(list,tuple)):
                methods = (methods,)

            for method in methods:
                self.__urls[method][url] = f
            
            self.__methods[url] = f

    def route(self,url,methods=[],accepts=MediaType.WILDCARD,produces=None):
        """Main decorator for registering REST functions """
        def wrap(f):
            self.__registerFunction(f, url, methods, accepts, produces)
            return f
        return wrap

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
        if request.path in self.__urls[request.method].keys():
            return self.__urls[request.method][request.path]()
        else:
            return self.__renderError(request,404,"URL '%s' not found\n" % request.path)
    
    def __renderError(self,request,code,message):
        """Common method for rendering errors"""
        request.setResponseCode(code)
        request.setHeader("content-type", MediaType.TEXT_PLAIN)
        return message
    
    def run(self,port=8080):
        """Shortcut for running app within Twisted reactor"""
        factory = Site(self)
        reactor.listenTCP(port, factory)    #@UndefinedVariable
        reactor.run()                       #@UndefinedVariable
        
    
    