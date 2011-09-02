'''
Argument extraction tests
@author: jacekf
'''

from corepost.web import CorePost, validate
from corepost.enums import Http
from formencode import Schema, validators

app = CorePost()

class TestSchema(Schema):
    allow_extra_fields = True
    childId = validators.Regex(regex="^jacekf|test$")

@app.route("/int/<int:intarg>/float/<float:floatarg>/string/<stringarg>",Http.GET)
def test(request,intarg,floatarg,stringarg,**kwargs):
    args = (intarg,floatarg,stringarg)
    return "%s" % map(lambda x: (type(x),x),args)

@app.route("/validate/<int:rootId>/schema",Http.POST)
@validate(schema=TestSchema)
def postValidateSchema(request,rootId,childId,**kwargs):
    return "%s - %s - %s" % (rootId,childId,kwargs)

@app.route("/validate/<int:rootId>/custom",Http.POST)
@validate(childId=validators.Regex(regex="^jacekf|test$"))
def postValidateCustom(request,rootId,childId,**kwargs):
    return "%s - %s - %s" % (rootId,childId,kwargs)

def run_app_arguments():
    app.run(8082)