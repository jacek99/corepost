'''
A RESTResource module1 that can be merged into the main RESTResource Resource
'''

from corepost.web import RESTResource, route
from corepost.enums import Http

class HomeApp():

    @route("/")
    def home_root(self,request,**kwargs):
        return "HOME %s" % kwargs

class Module1():
    path = "/module1"

    @route("/",Http.GET)
    def module1_get(self,request,**kwargs):
        return request.path
    
    @route("/sub",Http.GET)
    def module1e_sub(self,request,**kwargs):
        return request.path

class Module2():
    path = "/module2"
    
    @route("/",Http.GET)
    def module2_get(self,request,**kwargs):
        return request.path
    
    @route("/sub",Http.GET)
    def module2_sub(self,request,**kwargs):
        return request.path

def run_app_multi():
    app = RESTResource((HomeApp(),Module1(),Module2()))
    app.run(8081)
                   
if __name__ == "__main__":
    run_app_multi()