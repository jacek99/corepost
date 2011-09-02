'''
Argument extraction tests
@author: jacekf
'''

from corepost.web import CorePost
from corepost.enums import Http
from formencode import Schema, validators

app = CorePost()

@app.route("/int/<int:intarg>/float/<float:floatarg>/string/<stringarg>",Http.GET)
def test(request,intarg,floatarg,stringarg,**kwargs):
    args = (intarg,floatarg,stringarg)
    return "%s" % map(lambda x: (type(x),x),args)

@app.route("/validate/<int:rootId>/children",Http.POST)
@app.validate(childid=validators.String(not_empty=True))
def post(request,rootId,childId,**kwargs):
    return "%s - %s - %s" % (rootId,childId,kwargs)

def run_app_arguments():
    app.run(8082)