'''
A CorePost module1 that can be merged into the main CorePost Resource
'''

from corepost.web import CorePost
from corepost.enums import Http
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.server import Site

home = CorePost()

@home.route("/")
def home_root(request,**kwargs):
    return "HOME %s" % kwargs

module1 = CorePost('module1')

@module1.route("/",Http.GET)
def module1_get(request,**kwargs):
    return request.path

@module1.route("/sub",Http.GET)
def module1e_sub(request,**kwargs):
    return request.path

module2 = CorePost('module2')

@module2.route("/",Http.GET)
def module2_get(request,**kwargs):
    return request.path

@module2.route("/sub",Http.GET)
def module2_sub(request,**kwargs):
    return request.path

def run_app_multi():
    app = Resource()
    app.putChild(home.path, home)
    app.putChild(module1.path,module1)
    app.putChild(module2.path,module2)

    factory = Site(app)
    reactor.listenTCP(8081, factory)  #@UndefinedVariable
    reactor.run()                   #@UndefinedVariable
                   
