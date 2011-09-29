Twisted REST micro-framework
================================

Based on *Flask* API, with integrated multiprocessing support for full usage of all CPUs. 
Provides a more Flask/Sinatra-style API on top of the core *twisted.web* APIs.

Geared towards creating REST-oriented server platforms.
Tested on PyPy (recommended) and Python 2.7 for maximum performance.

Single REST module example
--------------------------

The simplest possible REST application:

    from corepost.web import CorePost, route
    from corepost.enums import Http
    
    class RestApp(CorePost):
    
        @route("/",Http.GET)
        def root(self,request,**kwargs):
            return request.path
        
        @route("/test",Http.GET)
        def test(self,request,**kwargs):
            return request.path
        
        @route("/test/<int:numericid>",Http.GET)
        def test_get_resources(self,request,numericid,**kwargs):
            return "%s" % numericid
    
    if __name__ == '__main__':
        app = RestApp()
        app.run()


Multi-module REST application
--------------------------------

The key CorePost object is just an extension of the regular twisted.web Resource object.
Therefore, it can easily be used to assemble a multi-module REST applications with
different CorePost resources serving from different context paths:

	from corepost.web import CorePost, route
	from corepost.enums import Http
	from twisted.web.resource import Resource
	from twisted.internet import reactor
	from twisted.web.server import Site
	
	class HomeApp(CorePost):
	
	    @route("/")
	    def home_root(self,request,**kwargs):
	        return "HOME %s" % kwargs
	
	class Module1(CorePost):
	
	    @route("/",Http.GET)
	    def module1_get(self,request,**kwargs):
	        return request.path
	    
	    @route("/sub",Http.GET)
	    def module1e_sub(self,request,**kwargs):
	        return request.path
	
	class Module2(CorePost):
	    
	    @route("/",Http.GET)
	    def module2_get(self,request,**kwargs):
	        return request.path
	    
	    @route("/sub",Http.GET)
	    def module2_sub(self,request,**kwargs):
	        return request.path
	
	def run_app_multi():
	    app = Resource()
	    app.putChild('', HomeApp())
	    app.putChild('module1',Module1())
	    app.putChild('module2',Module2())
	
	    factory = Site(app)
	    reactor.listenTCP(8081, factory)  #@UndefinedVariable
	    reactor.run()                   #@UndefinedVariable

The example above creates 3 modules ("/","module1","/module2") and exposes the following URLs:

	http://127.0.0.1:8080					
	http://127.0.0.1:8080/module1		
	http://127.0.0.1:8080/module1/sub		
	http://127.0.0.1:8080/module2			
	http://127.0.0.1:8080/module2/sub	

Path argument extraction
------------------------

CorePort can easily extract path arguments from an URL and convert them to the desired type.

The supported types are:

* *int*
* *float*
* *string*

Example:

	@route("/int/<int:intarg>/float/<float:floatarg>/string/<stringarg>",Http.GET)
	def test(self,request,intarg,floatarg,stringarg,**kwargs):
		pass

@defer.inlineCallbacks support
------------------------------

If you want a deferred async method, just use *defer.returnValue()*

	@route("/",Http.GET)
	@defer.inlineCallbacks
	def root(self,request,**kwargs):
		val1 = yield db.query("SELECT ....")
		val2 = yield db.query("SELECT ....")
		defer.returnValue(val1 + val2)
	    
Argument validation
-------------------

CorePost integrates the popular 'formencode' package to implement form and query argument validation.
Validators can be specified using a *formencode* Schema object, or via custom field-specific validators, e.g.:

	from corepost.web import CorePost, validate, route
	from corepost.enums import Http
	from formencode import Schema, validators

	class TestSchema(Schema):
	    allow_extra_fields = True
	    childId = validators.Regex(regex="^value1|value2$")
	
	class MyApp(CorePost):
		
		@route("/validate/<int:rootId>/schema",Http.POST)
		@validate(schema=TestSchema())
		def postValidateSchema(self,request,rootId,childId,**kwargs):
		    '''Validate using a common schema'''
		    return "%s - %s - %s" % (rootId,childId,kwargs)
		
		@route("/validate/<int:rootId>/custom",Http.POST)
		@validate(childId=validators.Regex(regex="^value1|value2$"))
		def postValidateCustom(self,request,rootId,childId,**kwargs):
		    '''Validate using argument-specific validators'
		    return "%s - %s - %s" % (rootId,childId,kwargs)	    

Please see the *FormEncode* <http://www.formencode.org/en/latest/Validator.html> documentation
for list of available validators:

* Common <http://www.formencode.org/en/latest/modules/validators.html#module-formencode.validators>
* National <http://www.formencode.org/en/latest/modules/national.html#module-formencode.national>

Content types
-------------

CorePost integrates support for JSON, YAML and XML (partially) based on request content types.

*Parsing of incoming content*

Based on the incoming content type in POST/PUT requests,
the body will be automatically parsed to JSON, YAML and XML (ElementTree) and attached to the request:

* request.json
* request.yaml
* request.xml

    @route("/post/json",(Http.POST,Http.PUT))
    def test_json(self,request,**kwargs):
        return "%s" % json.dumps(request.json)

    @route("/post/xml",(Http.POST,Http.PUT))
    def test_xml(self,request,**kwargs):
        return "%s" % ElementTree.tostring(request.xml)

    @route("/post/yaml",(Http.POST,Http.PUT))
    def test_yaml(self,request,**kwargs):
        return "%s" % yaml.dump(request.yaml)


*Routing requests by incoming content type*

Based on the incoming content type in POST/PUT requests,
the *same* URL can be hooked up to different router methods:

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

*Converting Python objects to content type based on what caller can accept*

Instead of returning string responses, the code can just return Python objects.
Depending whether the caller can accept JSON (default) or YAML, the Python objects	    
will be automatically converted:

    @route("/return/by/accept")
    def test_return_content_by_accepts(self,request,**kwargs):
        val = [{"test1":"Test1"},{"test2":"Test2"}]
        return val
        
Calling this URL with "Accept: application/json" will return:

	[{"test1": "Test1"}, {"test2": "Test2"}]
	
Calling it with "Accept: text/yaml" will return:

	- {test1: Test1}
	- {test2: Test2} 

*Note*: marshalling to XML will be supported in a future release. There is no default Python library that does this automatically.

HTTP codes
------------------

Success:

* 200 (OK) - GET, DELETE, PUT
* 201 (Created) - POST
	
Errors:

* 404 - not able to match any URL
* 400 - missing mandatory argument (driven from the arguments on the actual functions)
* 400 - argument failed validation
* 500 - server error
	    	        
Performance
-----------

On par with raw *twisted.web* performance. Minimal overhead for URL routing and function argument extraction.

BDD unit tests
--------------

All unit tests for CorePost are in BDD feature format, using Freshen.
Can be run using:

	nosetests --with-freshen -v

Plans
-----

* match all the relevant features of the Flask API
* integrate twisted.internet.processes in order to scale to multiple CPU cores : http://pypi.python.org/pypi/twisted.internet.processes
