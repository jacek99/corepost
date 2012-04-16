'''
Server tests
@author: jacekf
'''

from corepost.web import RESTResource, route
from corepost.enums import Http
from corepost.filters import IRequestFilter, IResponseFilter
from zope.interface import implements

class AddCustomHeaderFilter():
    """Implements just a request filter"""
    implements(IRequestFilter)
    
    def filterRequest(self,request):
        request.received_headers["Custom-Header"] = "Custom Header Value"

class Change404to503Filter():
    """Implements just a response filter that changes 404 to 503 statuses"""
    implements(IResponseFilter)
    
    def filterResponse(self,request,response):
        if response.code == 404:
            response.code = 503

class WrapAroundFilter():
    """Implements both types of filters in one class"""
    implements(IRequestFilter,IResponseFilter)

    def filterRequest(self,request):
        del(request.received_headers["user-agent"]) # remove this for unit tests, it varies from one box to another
        request.received_headers["X-Wrap-Input"] = "Input"
    
    def filterResponse(self,request,response):
        response.headers["X-Wrap-Output"] = "Output"

class FilterService():
    path = "/"
    
    @route("/",Http.GET)
    def root(self,request,**kwargs):
        return request.received_headers

def run_filter_app():
    app = RESTResource(services=(FilterService(),),filters=(Change404to503Filter(),AddCustomHeaderFilter(),WrapAroundFilter(),))
    app.run(8083)
    
if __name__ == "__main__":
    run_filter_app()