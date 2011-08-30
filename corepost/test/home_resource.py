'''
Server tests
@author: jacekf
'''

from corepost.web import CorePost
from corepost.enums import Http
from twisted.internet import defer

app = CorePost()

@app.route("/",Http.GET)
@defer.inlineCallbacks
def root(request,**kwargs):
    yield 1
    request.write("%s" % kwargs)
    request.finish()

@app.route("/test",Http.GET)
def test(request,**kwargs):
    return "%s" % kwargs

@app.route("/test/<int:numericid>/resource/<stringid>",Http.GET)
def test_get_resources(request,numericid,stringid,**kwargs):
    return "%s - %s" % (numericid,stringid)

@app.route("/post",(Http.POST,Http.PUT))
def test_post(request,**kwargs):
    return "%s" % kwargs

@app.route("/put",(Http.POST,Http.PUT))
def test_put(request,**kwargs):
    return "%s" % kwargs

@app.route("/postput",(Http.POST,Http.PUT))
def test_postput(request,**kwargs):
    return "%s" % kwargs

@app.route("/delete",Http.DELETE)
def test_delete(request,**kwargs):
    return "%s" % kwargs

def run_app_home():
    app.run()