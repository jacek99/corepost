'''
Created on 2011-10-03
@author: jacekf

Common routing classes, regardless of whether used in HTTP or multiprocess context
'''
from collections import defaultdict
from corepost import Response, RESTException
from corepost.enums import Http, HttpHeader
from corepost.utils import getMandatoryArgumentNames, convertToJson, safeDictUpdate
from corepost.convert import convertForSerialization, generateXml
from corepost.filters import IRequestFilter, IResponseFilter

from enums import MediaType
from twisted.internet import defer
from twisted.web.http import parse_qs
from twisted.python import log
import re, copy, exceptions, json, yaml, logging
from xml.etree import ElementTree

class UrlRouter:
    ''' Common class for containing info related to routing a request to a function '''
    
    __urlMatcher = re.compile(r"<(int|float|):?([^/]+)>")
    __urlRegexReplace = {"":r"(?P<arg>([^/]+))","int":r"(?P<arg>\d+)","float":r"(?P<arg>\d+.?\d*)"}
    __typeConverters = {"int":int,"float":float}
    
    def __init__(self,f,url,methods,accepts,produces,cache):
        self.__f = f
        self.__url = url
        self.__methods = methods if isinstance(methods,tuple) else (methods,)
        self.__accepts = accepts if isinstance(accepts,tuple) else (accepts,)
        self.__produces = produces
        self.__cache = cache
        self.__argConverters = {} # dict of arg names -> group index
        self.__validators = {}
        self.__mandatory = getMandatoryArgumentNames(f)[2:]
        
    def compileMatcherForFullUrl(self):
        """Compiles the regex matches once the URL has been updated to include the full path from the parent class"""
        #parse URL into regex used for matching
        m = UrlRouter.__urlMatcher.findall(self.url)
        self.__matchUrl = "^%s$" % self.url
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
    
    def __str__(self):
        return "%s %s" % (self.url, self.methods) 

class UrlRouterInstance():
    """Combines a UrlRouter with a class instance it should be executed against"""
    def __init__(self,clazz,urlRouter):
        self.clazz = clazz
        self.urlRouter = urlRouter
        
    def __str__(self):
        return self.urlRouter.url

class CachedUrl:
    '''
    Used for caching URLs that have been already routed once before. Avoids the overhead
    of regex processing on every incoming call for commonly accessed REST URLs
    '''
    def __init__(self,urlRouterInstance,args):
        self.__urlRouterInstance = urlRouterInstance
        self.__args = args
        
    @property
    def urlRouterInstance(self):
        return self.__urlRouterInstance
    
    @property
    def args(self):
        return self.__args
    
class RequestRouter:
    '''
    Class that handles request->method routing functionality to any type of resource
    '''
    
    def __init__(self,restServiceContainer,schema=None,filters=()):
        '''
        Constructor
        '''
        self.__urls = {Http.GET: defaultdict(dict),Http.POST: defaultdict(dict),Http.PUT: defaultdict(dict),Http.DELETE: defaultdict(dict)}
        self.__cachedUrls = {Http.GET: defaultdict(dict),Http.POST: defaultdict(dict),Http.PUT: defaultdict(dict),Http.DELETE: defaultdict(dict)}
        self.__urlRouterInstances = {}
        self.__schema = schema
        self.__registerRouters(restServiceContainer)
        self.__urlContainer = restServiceContainer
        self.__requestFilters = []
        self.__responseFilters = []
        
        #filters
        if filters != None:
            for webFilter in filters:
                valid = False
                if IRequestFilter.providedBy(webFilter):
                    self.__requestFilters.append(webFilter)
                    valid = True
                if IResponseFilter.providedBy(webFilter):
                    self.__responseFilters.append(webFilter)
                    valid = True
    
                if not valid:
                    raise RuntimeError("filter %s must implement IRequestFilter or IResponseFilter" % webFilter.__class__.__name__)

    @property
    def path(self):
        return self.__path    

    def __registerRouters(self,restServiceContainer):
        """Main method responsible for registering routers"""
        from types import FunctionType
        
        for service in restServiceContainer.services:
            # check if the service has a root path defined, which is optional
            rootPath = service.__class__.path if "path" in service.__class__.__dict__ else ""
            
            for key in service.__class__.__dict__:
                func = service.__class__.__dict__[key]
                # handle REST resources directly on the CorePost resource
                if type(func) == FunctionType and hasattr(func,'corepostRequestRouter'):
                    
                    # if specified, add class path to each function's path
                    rq = func.corepostRequestRouter
                    rq.url = "%s%s" % (rootPath,rq.url)
                    # remove first and trailing '/' to standardize URLs
                    start = 1 if rq.url[0:1] == "/" else 0
                    end =  -1 if rq.url[len(rq.url) -1] == '/' else len(rq.url)
                    rq.url = rq.url[start:end]
                     
                    # now that the full URL is set, compile the matcher for it
                    rq.compileMatcherForFullUrl()
                    
                    for method in rq.methods:
                        for accepts in rq.accepts:
                            urlRouterInstance = UrlRouterInstance(service,rq)
                            self.__urls[method][rq.url][accepts] = urlRouterInstance
                            self.__urlRouterInstances[func] = urlRouterInstance # needed so that we can lookup the urlRouterInstance for a specific function
                            

    def getResponse(self,request):
        """Finds the appropriate instance and dispatches the request to the registered function. Returns the appropriate Response object"""
        # see if already cached
        response = None
        try:
            if len(self.__requestFilters) > 0:
                self.__filterRequests(request)

            # standardize URL and remove trailing "/" if necessary
            standardized_postpath = request.postpath if (request.postpath[-1] != '' or request.postpath == ['']) else request.postpath[:-1]
            path = '/'.join(standardized_postpath) 

            contentType =  MediaType.WILDCARD if HttpHeader.CONTENT_TYPE not in request.received_headers else request.received_headers[HttpHeader.CONTENT_TYPE]       
                    
            urlRouterInstance, pathargs = None, None
            # fetch URL arguments <-> function from cache if hit at least once before
            if contentType in self.__cachedUrls[request.method][path]:
                cachedUrl = self.__cachedUrls[request.method][path][contentType]
                urlRouterInstance,pathargs = cachedUrl.urlRouterInstance, cachedUrl.args 
            else:
                # first time this URL is called
                instance = None

                # go through all the URLs, pick up the ones matching by content type
                # and then validate which ones match by path/argument to a particular UrlRouterInstance
                for contentTypeInstances in self.__urls[request.method].values():

                    if contentType in contentTypeInstances:
                        # there is an exact function for this incoming content type
                        instance = contentTypeInstances[contentType]
                    elif MediaType.WILDCARD in contentTypeInstances:
                        # fall back to any wildcard method
                        instance = contentTypeInstances[MediaType.WILDCARD]
                   
                    if instance != None:   
                        # see if the path arguments match up against any function @route definition
                        args = instance.urlRouter.getArguments(path)
                        if args != None:
                            if instance.urlRouter.cache:
                                self.__cachedUrls[request.method][path][contentType] = CachedUrl(instance, args)
                            urlRouterInstance,pathargs = instance,args
                            break
        
            #actual call
            if urlRouterInstance != None and pathargs != None:
                allargs = copy.deepcopy(pathargs)
                
                try:
                    # if POST/PUT, check if we need to automatically parse JSON, YAML, XML
                    self.__parseRequestData(request)
                    # parse request arguments from form or JSON docss
                    self.__addRequestArguments(request, allargs)
                    urlRouter = urlRouterInstance.urlRouter
                    val = urlRouter.call(urlRouterInstance.clazz,request,**allargs)
                 
                    #handle Deferreds natively
                    if isinstance(val,defer.Deferred):
                        # add callback to finish the request
                        val.addCallback(self.__finishDeferred,request)
                        val.addErrback(self.__finishDeferredError,request)
                        return val
                    else:
                        #special logic for POST to return 201 (created)
                        if request.method == Http.POST:
                            if hasattr(request, 'code'):
                                if request.code == 200:
                                    request.setResponseCode(201) 
                            else:
                                request.setResponseCode(201)
                        
                        response = self.__generateResponse(request, val, request.code)
                    
                except exceptions.TypeError as ex:
                    log.msg(ex,logLevel=logging.WARN)
                    response = self.__createErrorResponse(request,400,"%s" % ex)

                except RESTException as ex:
                    """Convert REST exceptions to their responses. Input errors log at a lower level to avoid overloading logs"""
                    if (ex.response.code in (400,404)):
                        log.msg(ex,logLevel=logging.WARN)
                    else:
                        log.err(ex)
                    response = ex.response

                except Exception as ex:
                    log.err(ex)
                    response =  self.__createErrorResponse(request,500,"Unexpected server error: %s\n%s" % (type(ex),ex))                
                
            else:
                log.msg("URL %s not found" % path,logLevel=logging.WARN)
                response = self.__createErrorResponse(request,404,"URL '%s' not found\n" % request.path)
        
        except Exception as ex:
            log.err(ex)
            response = self.__createErrorResponse(request,500,"Internal server error: %s" % ex)
        
        # response handling
        if response != None and len(self.__responseFilters) > 0:
            self.__filterResponses(request,response)

        return response
    
    def __generateResponse(self,request,response,code=200):
        """
        Takes care of automatically rendering the response and converting it to appropriate format (text,XML,JSON,YAML)
        depending on what the caller can accept. Returns Response
        """
        if isinstance(response, str):
            return Response(code,response,{HttpHeader.CONTENT_TYPE: MediaType.TEXT_PLAIN})
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
                return (generateXml(obj),MediaType.APPLICATION_XML)
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

    def __finishDeferredError(self,error,request):
        """Finishes any Defered/inlineCallback methods that raised an error. Returns Response"""
        log.err(error, "Deferred failed")
        return self.__createErrorResponse(request, 500,"Internal server error")
    
    def __createErrorResponse(self,request,code,message):
        """Common method for rendering errors"""
        return Response(code=code, entity=message, headers={"content-type": MediaType.TEXT_PLAIN})
 
    def __parseRequestData(self,request):
        '''Automatically parses JSON,XML,YAML if present'''
        if request.method in (Http.POST,Http.PUT) and HttpHeader.CONTENT_TYPE in request.received_headers.keys():
            contentType = request.received_headers["content-type"]
            if contentType == MediaType.APPLICATION_JSON:
                try:
                    request.json = json.loads(request.content.read())
                except Exception as ex:
                    raise TypeError("Unable to parse JSON body: %s" % ex)
            elif contentType in (MediaType.APPLICATION_XML,MediaType.TEXT_XML):
                try: 
                    request.xml = ElementTree.XML(request.content.read())
                except Exception as ex:
                    raise TypeError("Unable to parse XML body: %s" % ex)
            elif contentType == MediaType.TEXT_YAML:
                try: 
                    request.yaml = yaml.safe_load(request.content.read())
                except Exception as ex:
                    raise TypeError("Unable to parse YAML body: %s" % ex)

    def __addRequestArguments(self,request,allargs):
        """Parses the request form arguments OR JSON document root elements to build the list of arguments to a method"""
        # handler for weird Twisted logic where PUT does not get form params
        # see: http://twistedmatrix.com/pipermail/twisted-web/2007-March/003338.html
        requestargs = request.args
        if request.method == Http.PUT and HttpHeader.CONTENT_TYPE in request.received_headers.keys() \
            and request.received_headers[HttpHeader.CONTENT_TYPE] == MediaType.APPLICATION_FORM_URLENCODED:
            requestargs = parse_qs(request.content.read(), 1)
        
        #merge form args
        if len(requestargs.keys()) > 0:
            for arg in requestargs.keys():
                # maintain first instance of an argument always
                safeDictUpdate(allargs,arg,requestargs[arg][0])
        elif hasattr(request,'json'):
            # if YAML parse root elements instead of form elements   
            for key in request.json.keys():
                safeDictUpdate(allargs, key, request.json[key])
        elif hasattr(request,'yaml'):
            # if YAML parse root elements instead of form elements   
            for key in request.yaml.keys():
                safeDictUpdate(allargs, key, request.yaml[key])
        elif hasattr(request,'xml'):
            # if XML, parse attributes first, then root nodes
            for key in request.xml.attrib:
                safeDictUpdate(allargs, key, request.xml.attrib[key])
            for el in request.xml.findall("*"):
                safeDictUpdate(allargs, el.tag,el.text)
        
            
    def __filterRequests(self,request):
        """Filters incoming requests"""
        for webFilter in self.__requestFilters:
            webFilter.filterRequest(request)
            
    def __filterResponses(self,request,response):
        """Filters incoming requests"""
        for webFilter in self.__responseFilters:
            webFilter.filterResponse(request,response)            