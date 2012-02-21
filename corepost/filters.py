'''
Various filters & interceptors
@author: jacekf
'''
from zope.interface import Interface

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
