'''
Server tests
@author: jacekf
'''

from corepost.server import CorePost
from corepost.enums import Http

app = CorePost()

@app.route("/",Http.GET)
def root(request,**kwargs):
    return "%s" % kwargs

@app.route("/test",Http.GET)
def test(request,**kwargs):
    return "%s" % kwargs

@app.route("/test/<int:jacek>/yo/<someid>",Http.GET)
def test_get_resources(request,jacek,someid,**kwargs):
    return "%s - %s" % (jacek,someid)

@app.route("/test",Http.POST)
def test_post(request,**kwargs):
    return "%s" % kwargs

if __name__ == '__main__':
    app.run()