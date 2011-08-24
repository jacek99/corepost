'''
Server tests
@author: jacekf
'''

from corepost.server import CorePost
from corepost.enums import Http

app = CorePost()

@app.route("/",Http.GET)
def root(request):
    return request.path

@app.route("/test",Http.GET)
def test(request):
    return request.path

@app.route("/test/<int:jacek>/yo/<someid>",Http.GET)
def test_get_resources(request,jacek,someid,**kwargs):
    return "%s - %s" % (jacek,someid)

if __name__ == '__main__':
    app.run()