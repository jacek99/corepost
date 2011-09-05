'''
A CorePost module1 that can be merged into the main CorePost Resource
'''

from corepost.web import CorePost, route
from corepost.enums import Http
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.server import Site

class HomeApp(CorePost):

    @route("/")
    def home_root(self,request,**kwargs):
        return "HOME %s" % kwargs

class Module1(CorePost):

    @route("/",Http.GET)
    def module1_get(self,request,**kwargs):
        return request.path
    
    @route("/sub",Http.GET)
    def module1e_sub(self,request,**kwargs):
        return request.path

class Module2(CorePost):
    
    @route("/",Http.GET)
    def module2_get(self,request,**kwargs):
        return request.path
    
    @route("/sub",Http.GET)
    def module2_sub(self,request,**kwargs):
        return request.path

def run_app_multi():
    app = Resource()
    app.putChild('', HomeApp())
    app.putChild('module1',Module1())
    app.putChild('module2',Module2())

    factory = Site(app)
    reactor.listenTCP(8081, factory)  #@UndefinedVariable
    reactor.run()                   #@UndefinedVariable
                   
