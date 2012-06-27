'''
Server tests
@author: jacekf
'''

from corepost.web import RESTResource, route
from corepost.enums import Http, MediaType, HttpHeader
from twisted.internet import defer
from xml.etree import ElementTree
import json, yaml

class HomeApp():
    
    def __init__(self,*args,**kwargs):
        self.issue1 = "issue 1"
    
    @route("/",Http.GET)
    @defer.inlineCallbacks
    def root(self,request,**kwargs):
        yield 1
        request.write("%s" % kwargs)
        request.finish()
    
    @route("/test",Http.GET)
    def test(self,request,**kwargs):
        return "%s" % kwargs
    
    @route("/test/<int:numericid>/resource/<stringid>",Http.GET)
    def test_get_resources(self,request,numericid,stringid,**kwargs):
        return "%s - %s" % (numericid,stringid)
    
    @route("/post",(Http.POST,Http.PUT))
    def test_post(self,request,**kwargs):
        return "%s" % kwargs
    
    @route("/put",(Http.POST,Http.PUT))
    def test_put(self,request,**kwargs):
        return "%s" % kwargs
    
    @route("/postput",(Http.POST,Http.PUT))
    def test_postput(self,request,**kwargs):
        return "%s" % kwargs
    
    @route("/delete",Http.DELETE)
    def test_delete(self,request,**kwargs):
        return "%s" % kwargs
    
    @route("/post/json",(Http.POST,Http.PUT))
    def test_json(self,request,**kwargs):
        return "%s" % json.dumps(request.json)

    @route("/post/xml",(Http.POST,Http.PUT))
    def test_xml(self,request,**kwargs):
        return "%s" % ElementTree.tostring(request.xml)

    @route("/post/yaml",(Http.POST,Http.PUT))
    def test_yaml(self,request,**kwargs):
        return "%s" % yaml.dump(request.yaml,indent=4,width=130,default_flow_style=False)

    ##################################################################
    # same URLs, routed by incoming content type
    ###################################################################
    @route("/post/by/content",(Http.POST,Http.PUT),MediaType.APPLICATION_JSON)
    def test_content_app_json(self,request,**kwargs):
        return request.received_headers[HttpHeader.CONTENT_TYPE]

    @route("/post/by/content",(Http.POST,Http.PUT),(MediaType.TEXT_XML,MediaType.APPLICATION_XML))
    def test_content_xml(self,request,**kwargs):
        return request.received_headers[HttpHeader.CONTENT_TYPE]

    @route("/post/by/content",(Http.POST,Http.PUT),MediaType.TEXT_YAML)
    def test_content_yaml(self,request,**kwargs):
        return request.received_headers[HttpHeader.CONTENT_TYPE]

    @route("/post/by/content",(Http.POST,Http.PUT))
    def test_content_catch_all(self,request,**kwargs):
        return MediaType.WILDCARD
    
    ##################################################################
    # one URL, serving different content types
    ###################################################################
    @route("/return/by/accept")
    def test_return_content_by_accepts(self,request,**kwargs):
        val = [{"test1":"Test1"},{"test2":"Test2"}]
        return val

    @route("/return/by/accept/deferred")
    @defer.inlineCallbacks
    def test_return_content_by_accept_deferred(self,request,**kwargs):
        """Ensure support for inline callbacks and deferred"""
        val = yield [{"test1":"Test1"},{"test2":"Test2"}]
        defer.returnValue(val) 

    @route("/return/by/accept/class")
    def test_return_class_content_by_accepts(self,request,**kwargs):
        """Uses Python class instead of dict/list"""
        
        class TestReturn:
            """Test return class"""
            def __init__(self):
                self.__t1 = 'Test'
        
        t1 = TestReturn()
        t1.test1 = 'Test1'
        
        t2 = TestReturn()
        t2.test2="Test2"
        return (t1,t2)

    ####################################
    # Issues
    ####################################
    @route("/issues/1")
    def test_issue_1(self,request,**kwargs):
        return self.issue1

    ####################################
    # extra HTTP methods
    ####################################
    @route("/methods/head",Http.HEAD)
    def test_head_http(self,request,**kwargs):
        return ""

    @route("/methods/options",Http.OPTIONS)
    def test_options_http(self,request,**kwargs):
        return "OPTIONS"

    @route("/methods/patch",Http.PATCH)
    def test_patch_http(self,request,**kwargs):
        return "PATCH=%s" % kwargs

def run_app_home():
    app = RESTResource((HomeApp(),))
    app.run()
    
if __name__ == "__main__":
    run_app_home()