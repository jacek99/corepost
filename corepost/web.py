'''
Main server classes

@author: jacekf
'''
import re, copy
from twisted.internet import reactor, defer
from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.http import parse_qs
from collections import defaultdict
from enums import MediaType
from corepost.enums import Http
    
class RequestRouter:
    """ Common class for containing info related to routing a request to a function """
    
    __urlMatcher = re.compile(r"<(int|float|):?([a-zA-Z0-9]+)>")
    __urlRegexReplace = {"":r"(?P<arg>.+)","int":r"(?P<arg>\d+)","float":r"(?P<arg>\d+.?\d*)"}
    __typeConverters = {"int":int,"float":float}
    
    def __init__(self,f,url,method,accepts,produces,cache):
        self.__url = url
        self.__method = method
        self.__accepts = accepts
        self.__produces = produces
        self.__cache = cache
        self.__f = f
        self.__argConverters = {} # dict of arg names -> group index
        
        #parse URL into regex used for matching
        m = RequestRouter.__urlMatcher.findall(url)
        
        self.__matchUrl = "^%s$" % url
        for match in m:
            if len(match[0]) == 0:
                # string
                self.__argConverters[match[1]] = None
                self.__matchUrl = self.__matchUrl.replace("<%s>" % match[1],
                                    RequestRouter.__urlRegexReplace[match[0]].replace("arg",match[1]))
            else:
                # non string
                self.__argConverters[match[1]] = RequestRouter.__typeConverters[match[0]]
                self.__matchUrl = self.__matchUrl.replace("<%s:%s>" % match,
                                    RequestRouter.__urlRegexReplace[match[0]].replace("arg",match[1]))

        self.__matcher = re.compile(self.__matchUrl)
        
    @property
    def cache(self):
        """Indicates if this URL should be cached or not"""
        return self.__cache    
        
    def getArguments(self,url):
        """
        Returns None if nothing matched (i.e. URL does not match), empty dict if no args found (i,e, static URL)
        or dict with arg/values for dynamic URLs
        """
        g = self.__matcher.search(url)
        if g != None:
            args = g.groupdict()
            # convert to expected datatypes
            if len(args) > 0:
                for name in args.keys():
                    converter = self.__argConverters[name]
                    if converter != None:
                        args[name] = converter(args[name])
            return args
        else:
            return None
        
    def call(self,request,**kwargs):
        """Forwards call to underlying method"""
        return self.__f(request,**kwargs)

class CachedUrl():
    """
    Used for caching URLs that have been already routed once before. Avoids the overhead
    of regex processing on every incoming call for commonly accessed REST URLs
    """
    def __init__(self,router,args):
        self.__router = router
        self.__args = args
        
    @property
    def router(self):
        return self.__router
    
    @property
    def args(self):
        return self.__args
    
class CorePost(Resource):
    '''
    Main resource responsible for routing REST requests to the implementing methods
    '''
    isLeaf = True
    
    def __init__(self):
        '''
        Constructor
        '''
        Resource.__init__(self)
        self.__urls = defaultdict(dict)
        self.__cachedUrls = defaultdict(dict)
        self.__methods = {}

    def __registerFunction(self,f,url,methods,accepts,produces,cache):
        if f not in self.__methods.values():
            if not isinstance(methods,(list,tuple)):
                methods = (methods,)

            for method in methods:
                rq = RequestRouter(f, url, method, accepts, produces,cache)
                self.__urls[method][url] = rq
            
            self.__methods[url] = f

    def route(self,url,methods=[],accepts=MediaType.WILDCARD,produces=None,cache=True):
        """Main decorator for registering REST functions """
        def wrap(f):
            self.__registerFunction(f, url, methods, accepts, produces,cache)
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
        """Finds the appropriate router and dispatches the request to the registered function"""
        # see if already cached
        path = '/' + '/'.join(request.postpath)
        
        urlrouter, pathargs = None, None
        if path in self.__cachedUrls[request.method]:
            cachedUrl = self.__cachedUrls[request.method][path]
            urlrouter,pathargs = cachedUrl.router, cachedUrl.args 
        else:
            # first time this URL is called
            for router in self.__urls[request.method].values():
                args = router.getArguments(path)
                if args != None:
                    if router.cache:
                        self.__cachedUrls[request.method][path] = CachedUrl(router, args)
                    urlrouter,pathargs = router,args
                    
        #actual call
        if urlrouter != None and pathargs != None:
            allargs = copy.deepcopy(pathargs)
            # handler for weird Twisted logic where PUT does not get form params
            # see: http://twistedmatrix.com/pipermail/twisted-web/2007-March/003338.html
            requestargs = request.args
            if request.method == Http.PUT:
                requestargs = parse_qs(request.content.read(), 1)

            #merge form args
            for arg in requestargs.keys():
                # maintain first instance of an argument always
                if arg not in allargs:
                    allargs[arg] = requestargs[arg][0]
                    
            # if POST/PUT, check if we need to automatically parse JSON
            # TODO
            
            #handle Deferreds natively
            
            val = urlrouter.call(request,**allargs)
            if isinstance(val,defer.Deferred):
                # we assume the method will call request.finish()
                return NOT_DONE_YET
            else:
                return val
            
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
        
    
    