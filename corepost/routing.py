'''
Created on 2011-10-03
@author: jacekf

Common routing classes, regardless of whether used in HTTP or ZeroMQ context
'''
from collections import defaultdict
from corepost.enums import Http, HttpHeader
from corepost.utils import getMandatoryArgumentNames, convertToJson
from corepost.convert import convertForSerialization, generateXml
from corepost import Response
from enums import MediaType
from formencode import FancyValidator, Invalid
from twisted.internet import reactor, defer
from twisted.web.http import parse_qs
from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET
import re, copy, exceptions, json, yaml
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

class UrlRouter:
    ''' Common class for containing info related to routing a request to a function '''
    
    __urlMatcher = re.compile(r"<(int|float|):?([a-zA-Z0-9]+)>")
    __urlRegexReplace = {"":r"(?P<arg>.+)","int":r"(?P<arg>\d+)","float":r"(?P<arg>\d+.?\d*)"}
    __typeConverters = {"int":int,"float":float}
    
    def __init__(self,f,url,methods,accepts,produces,cache):
        self.__url = url
        self.__methods = methods if isinstance(methods,tuple) else (methods,)
        self.__accepts = accepts if isinstance(accepts,tuple) else (accepts,)
        self.__produces = produces
        self.__cache = cache
        self.__f = f
        self.__argConverters = {} # dict of arg names -> group index
        self.__validators = {}
        self.__mandatory = getMandatoryArgumentNames(f)[2:]
        
        #parse URL into regex used for matching
        m = UrlRouter.__urlMatcher.findall(url)
        
        self.__matchUrl = "^%s$" % url
        for match in m:
            if len(match[0]) == 0:
                # string
                self.__argConverters[match[1]] = None
                self.__matchUrl = self.__matchUrl.replace("<%s>" % match[1],
                                    UrlRouter.__urlRegexReplace[match[0]].replace("arg",match[1]))
            else:
                # non string
                self.__argConverters[match[1]] = UrlRouter.__typeConverters[match[0]]
                self.__matchUrl = self.__matchUrl.replace("<%s:%s>" % match,
                                    UrlRouter.__urlRegexReplace[match[0]].replace("arg",match[1]))

        self.__matcher = re.compile(self.__matchUrl)
        
    @property
    def cache(self):
        '''Indicates if this URL should be cached or not'''
        return self.__cache    

    @property
    def methods(self):
        return self.__methods
    
    @property
    def url(self):
        return self.__url

    @property
    def accepts(self):
        return self.__accepts

    def addValidator(self,fieldName,validator):
        '''Adds additional field-specific formencode validators'''
        self.__validators[fieldName] = validator
        
    def getArguments(self,url):
        '''
        Returns None if nothing matched (i.e. URL does not match), empty dict if no args found (i,e, static URL)
        or dict with arg/values for dynamic URLs
        '''
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
        
    def call(self,instance,request,**kwargs):
        '''Forwards call to underlying method'''
        for arg in self.__mandatory:
            if arg not in kwargs:
                raise TypeError("Missing mandatory argument '%s'" % arg)
        return self.__f(instance,request,**kwargs)

class CachedUrl:
    '''
    Used for caching URLs that have been already routed once before. Avoids the overhead
    of regex processing on every incoming call for commonly accessed REST URLs
    '''
    def __init__(self,router,args):
        self.__router = router
        self.__args = args
        
    @property
    def router(self):
        return self.__router
    
    @property
    def args(self):
        return self.__args
    
class RequestRouter:
    '''
    Class that handles request->method routing functionality to any type of resource
    '''
    
    def __init__(self,urlContainer,schema=None):
        '''
        Constructor
        '''
        self.__urls = {Http.GET: defaultdict(dict),Http.POST: defaultdict(dict),Http.PUT: defaultdict(dict),Http.DELETE: defaultdict(dict)}
        self.__cachedUrls = {Http.GET: defaultdict(dict),Http.POST: defaultdict(dict),Http.PUT: defaultdict(dict),Http.DELETE: defaultdict(dict)}
        self.__routers = {}
        self.__schema = schema
        self.__registerRouters(urlContainer)
        self.__urlContainer = urlContainer

    @property
    def path(self):
        return self.__path    

    def __registerRouters(self,urlContainer):
        """Main method responsible for registering routers"""
        from types import FunctionType
        for _,func in urlContainer.__class__.__dict__.iteritems():
            if type(func) == FunctionType and hasattr(func,'corepostRequestRouter'):
                rq = func.corepostRequestRouter
                for method in rq.methods:
                    for accepts in rq.accepts:
                        self.__urls[method][rq.url][accepts] = rq
                        self.__routers[func] = rq # needed so that we cdan lookup the router for a specific function

    def route(self,url,methods=(Http.GET,),accepts=MediaType.WILDCARD,produces=None,cache=True):
        '''Obsolete'''
        raise RuntimeError("Do not @app.route() any more, as of 0.0.6 API has been re-designed around class methods, see docs and examples")

    def getResponse(self,request):
        """Finds the appropriate router and dispatches the request to the registered function. Returns the appropriate Response object"""
        # see if already cached
        try:
            path = '/' + '/'.join(request.postpath)
            contentType =  MediaType.WILDCARD if HttpHeader.CONTENT_TYPE not in request.received_headers else request.received_headers[HttpHeader.CONTENT_TYPE]       
                    
            urlrouter, pathargs = None, None
            # fetch URL arguments <-> function from cache if hit at least once before
            if contentType in self.__cachedUrls[request.method][path]:
                cachedUrl = self.__cachedUrls[request.method][path][contentType]
                urlrouter,pathargs = cachedUrl.router, cachedUrl.args 
            else:
                # first time this URL is called
                router = None

                for contentTypeFunctions in self.__urls[request.method].values():

                    if contentType in contentTypeFunctions:
                        # there is an exact function for this incoming content type
                        router = contentTypeFunctions[contentType]
                    elif MediaType.WILDCARD in contentTypeFunctions:
                        # fall back to any wildcard method
                        router = contentTypeFunctions[MediaType.WILDCARD]
                   
                    if router != None:   
                        # see if the path arguments match up against any function @route definition
                        args = router.getArguments(path)
                        if args != None:
                            if router.cache:
                                self.__cachedUrls[request.method][path][contentType] = CachedUrl(router, args)
                            urlrouter,pathargs = router,args
                            break
                        
            #actual call
            if urlrouter != None and pathargs != None:
                allargs = copy.deepcopy(pathargs)
                # handler for weird Twisted logic where PUT does not get form params
                # see: http://twistedmatrix.com/pipermail/twisted-web/2007-March/003338.html
                requestargs = request.args
                if request.method == Http.PUT and HttpHeader.CONTENT_TYPE in request.received_headers.keys() \
                    and request.received_headers[HttpHeader.CONTENT_TYPE] == MediaType.APPLICATION_FORM_URLENCODED:
                    requestargs = parse_qs(request.content.read(), 1)
    
                #merge form args
                for arg in requestargs.keys():
                    # maintain first instance of an argument always
                    if arg not in allargs:
                        allargs[arg] = requestargs[arg][0]
                
                try:
                    # if POST/PUT, check if we need to automatically parse JSON
                    self.__parseRequestData(request)
                    val = urlrouter.call(self.__urlContainer,request,**allargs)
                 
                    #handle Deferreds natively
                    if isinstance(val,defer.Deferred):
                        # add callback to finish the request
                        val.addCallback(self.__finishDeferred,request)
                        return val
                    else:
                        #special logic for POST to return 201 (created)
                        if request.method == Http.POST:
                            if hasattr(request, 'code'):
                                if request.code == 200:
                                    request.setResponseCode(201) 
                            else:
                                request.setResponseCode(201)
                        
                        return self.__generateResponse(request, val, request.code)
                    
                except exceptions.TypeError as ex:
                    return self.__createErrorResponse(request,400,"%s" % ex)
                except Exception as ex:
                    return self.__createErrorResponse(request,500,"Unexpected server error: %s\n%s" % (type(ex),ex))                
                
            else:
                return self.__createErrorResponse(request,404,"URL '%s' not found\n" % request.path)
        
        except Exception as ex:
            return self.__createErrorResponse(request,500,"Internal server error: %s" % ex)
    
    def __generateResponse(self,request,response,code=200):
        """
        Takes care of automatically rendering the response and converting it to appropriate format (text,XML,JSON,YAML)
        depending on what the caller can accept. Returns Response
        """
        if isinstance(response, str):
            return Response(code,response,{HttpHeader.CONTENT_TYPE:MediaType.TEXT_PLAIN})
        elif isinstance(response, Response):
            return response
        else:
            (content,contentType) = self.__convertObjectToContentType(request, response)
            return Response(code,content,{HttpHeader.CONTENT_TYPE:contentType})

    def __convertObjectToContentType(self,request,obj):
        """
        Takes care of converting an object (non-String) response to the appropriate format, based on the what the caller can accept.
        Returns a tuple of (content,contentType)
        """
        obj = convertForSerialization(obj)
        
        if HttpHeader.ACCEPT in request.received_headers:
            accept = request.received_headers[HttpHeader.ACCEPT]
            if MediaType.APPLICATION_JSON in accept:
                return (convertToJson(obj),MediaType.APPLICATION_JSON)
            elif MediaType.TEXT_YAML in accept:
                return (yaml.dump(obj),MediaType.TEXT_YAML)
            elif MediaType.APPLICATION_XML in accept or MediaType.TEXT_XML in accept:
                return (generateXml(obj),MediaType.APPLICATION_XML+";charset=utf-8")
            else:
                # no idea, let's do JSON
                return (convertToJson(obj),MediaType.APPLICATION_JSON)
        else:
            # called has no accept header, let's default to JSON
            return (convertToJson(obj),MediaType.APPLICATION_JSON)

    def __finishDeferred(self,val,request):
        """Finishes any Defered/inlineCallback methods. Returns Response"""
        if isinstance(val,Response):
            return val
        elif val != None:
            try:
                return self.__generateResponse(request,val)
            except Exception as ex:
                msg = "Unexpected server error: %s\n%s" % (type(ex),ex)
                return self.__createErrorResponse(request, 500, msg)
        else:
            return Response(209,None)
    
    def __createErrorResponse(self,request,code,message):
        """Common method for rendering errors"""
        return Response(code=code, entity=message, headers={"content-type": MediaType.TEXT_PLAIN})
 
    def __parseRequestData(self,request):
        '''Automatically parses JSON,XML,YAML if present'''
        if request.method in (Http.POST,Http.PUT) and HttpHeader.CONTENT_TYPE in request.received_headers.keys():
            type = request.received_headers["content-type"]
            if type == MediaType.APPLICATION_JSON:
                try:
                    request.json = json.loads(request.content.read())
                except Exception as ex:
                    raise TypeError("Unable to parse JSON body: %s" % ex)
            elif type in (MediaType.APPLICATION_XML,MediaType.TEXT_XML):
                try: 
                    request.xml = ElementTree.XML(request.content.read())
                except Exception as ex:
                    raise TypeError("Unable to parse XML body: %s" % ex)
            elif type == MediaType.TEXT_YAML:
                try: 
                    request.yaml = yaml.safe_load(request.content.read())
                except Exception as ex:
                    raise TypeError("Unable to parse YAML body: %s" % ex)
