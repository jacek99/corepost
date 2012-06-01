'''
ZeroMQ resource

@author: jacekf
'''

from corepost.web import RESTResource, route
from corepost.enums import Http
from corepost.filters import IRequestFilter, IResponseFilter
from zope.interface import implements

from multiprocessing import Pool

class TestService:
    
    @route("/")
    def forward(self,request):
        return ""
    
def startClient():
    return "TEST"
    

def run_app_multicore():
    #start the ZeroMQ client
    pool = Pool(processes=4)
    
    #start the server
    app = RESTResource((TestService(),))
    app.run(8090)
                   
if __name__ == "__main__":
    run_app_multicore()    
    
    