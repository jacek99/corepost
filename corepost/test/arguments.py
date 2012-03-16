'''
Argument extraction tests
@author: jacekf
'''

from corepost.web import RESTResource, validate, route
from corepost.enums import Http
from formencode import Schema, validators

class TestSchema(Schema):
    allow_extra_fields = True
    childId = validators.Regex(regex="^jacekf|test$")

class ArgumentApp():
    
    @route("/int/<int:intarg>/float/<float:floatarg>/string/<stringarg>",Http.GET)
    def test(self,request,intarg,floatarg,stringarg,**kwargs):
        args = (intarg,floatarg,stringarg)
        return "%s" % map(lambda x: (type(x),x),args)
    
    @route("/validate/<int:rootId>/schema",Http.POST)
    @validate(schema=TestSchema())
    def postValidateSchema(self,request,rootId,childId,**kwargs):
        return "%s - %s - %s" % (rootId,childId,kwargs)
    
    @route("/validate/<int:rootId>/custom",Http.POST)
    @validate(childId=validators.Regex(regex="^jacekf|test$"))
    def postValidateCustom(self,request,rootId,childId,**kwargs):
        return "%s - %s - %s" % (rootId,childId,kwargs)

    @route("/formOrJson",(Http.POST,Http.PUT))
    def postArgumentsByContentType(self,request,first,last,**kwargs):
        return "%s %s" % (str(first),str(last))


def run_app_arguments():
    app = RESTResource((ArgumentApp(),))
    app.run(8082)