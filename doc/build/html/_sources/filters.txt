Filters
=======

There is support for CorePost resource filters via the two following *corepost.filter* interfaces::

	class IRequestFilter(Interface):
	    """Request filter interface"""    
	    def filterRequest(self,request):
	        """Allows to intercept and change an incoming request"""
	        pass
	
	class IResponseFilter(Interface):
	    """Response filter interface"""
	    def filterResponse(self,request,response):
	        """Allows to intercept and change an outgoing response"""
	        pass

A filter class can implement either of them or both (for a wrap around filter), e.g.::

	class AddCustomHeaderFilter():
	    """Implements a request filter that adds a custom header to the incoming request"""
	    zope.interface.implements(IRequestFilter)
	    
	    def filterRequest(self,request):
	        request.received_headers["Custom-Header"] = "Custom Header Value"
	
	class Change404to503Filter():
	    """Implements just a response filter that changes 404 to 503 statuses"""
	    zope.interface.implements(IResponseFilter)
	    
	    def filterResponse(self,request,response):
	        if response.code == 404:
	            response.code = 503

	class WrapAroundFilter():
	    """Implements both types of filters in one class"""
	    zope.interface.implements(IRequestFilter,IResponseFilter)
	
	    def filterRequest(self,request):
	        request.received_headers["X-Wrap-Input"] = "Input"
	    
	    def filterResponse(self,request,response):
	        response.headers["X-Wrap-Output"] = "Output"


In order to activate the filters on a RESTResource instance, you need to pass a list of them in the constructor as the *filters* parameter, e.g.::
 	   
	class FilterApp:
	    
	    @route("/",Http.GET)
	    def root(self,request,**kwargs):
	        return request.received_headers
	
	def run_filter_app():
	    app = RESTResource(services=(FilterApp(),),filters=(Change404to503Filter(),AddCustomHeaderFilter(),WrapAroundFilter(),))
	    app.run(8083)

