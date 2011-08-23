'''
Created on 2011-08-23

@author: jacekf
'''
import re
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
    
    __urlMatcher = re.compile(r"<(int|float|):?([a-zA-Z0-9]+)>")
    __urlRegexReplace = {"":r"(.+)","int":r"(d+)","float":r"(d+\.d+)"}
    
    """ Common class for containing info related to routing a request to a function """
    def __init__(self,f,url,method,accepts,produces):
        self.__url = url
        self.__method = method
        self.__accepts = accepts
        self.__produces = produces
        self.__f = f
        self.__args = [] # dict of arg names -> group index
        
        #parse URL into regex used for matching
        m = RequestRouter.__urlMatcher.findall(url)
        
        self.__matchUrl = url
        for match in m:
            self.__args.append(match[1])
            if len(match[0]) == 0:
                # string
                self.__matchUrl = self.__matchUrl.replace("<%s>" % match[1],RequestRouter.__urlRegexReplace[match[0]])
            else:
                # non string
                self.__matchUrl = self.__matchUrl.replace("<%s:%s>" % match,RequestRouter.__urlRegexReplace[match[0]])

        self.__matcher = re.compile(self.__matchUrl)
        
    def getMatch(self,url):
        return self.__matcher.findall(url)
        
    def call(self,**kwargs):
        self.__f(**kwargs)
    
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
                rq = RequestRouter(f, url, method, accepts, produces)
            
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
        
    
    