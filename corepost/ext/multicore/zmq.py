__author__ = 'jacekf'

try:
    import txZMQ
except ImportError as ex:
    print "You must have ZeroMQ and txZMQ installed"
    raise ex

from corepost import Response, IRESTResource
from corepost.enums import Http
from corepost.routing import UrlRouter, RequestRouter
from enums import MediaType
from formencode import FancyValidator, Invalid
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET
from zope.interface import implements

class ZMQResource(Resource):
    """
    Responsible for intercepting HTTP requests and marshalling them via ZeroMQ to responders in the process pool
    """
    isLeaf = True
    implements(IRESTResource)

    def __init__(self):
        '''
        Constructor
        '''
        Resource.__init__(self)

    def render(self, request):
        """Posts request to ZeroMQ and waits for response"""
        pass


class ZMQResponder:
    """
    Responsible for processing an incoming request via ZeroMQ and responding via a REST API as if it were a direct HTTP request
    """
    def __init__(self,services=(),schema=None,filters=()):
        '''
        Constructor
        '''
        self.services = services
        self.__router = RequestRouter(self,schema,filters)
