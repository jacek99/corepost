Twisted REST micro-framework
================================

Based on *Flask* API, with integrated multiprocessing support for full usage of all CPUs. 
Provides a more Flask/Sinatra-style API on top of the core *twisted.web* APIs.

Geared towards creating REST-oriented server platforms.
Tested on PyPy (recommended) and Python 2.7 for maximum performance.

Single REST module example
--------------------------

The simplest possible REST application:

	from corepost.web import CorePost
	from corepost.enums import Http
	
	app = CorePost()
	
	@app.route("/",Http.GET)
	def root(request,**kwargs):
	    return request.path
	
	@app.route("/test",Http.GET)
	def test(request,**kwargs):
	    return request.path
	
	@app.route("/test/<int:numericid>/test2/<stringid>",Http.GET)
	def test_get_resources(request,numericid,stringid,**kwargs):
	    return "%s - %s" % (numericid,stringid)
	
	if __name__ == '__main__':
	    # shortcut method to run a CorePost Resource as a single site
	    app.run()


Multi-module REST application
--------------------------------

The key CorePost object is just an extension of the regular twisted.web Resource object.
Therefore, it can easily be used to assemble a multi-module REST applications with
different CorePost resources serving from different context paths:

    from corepost.web import CorePost
    from corepost.enums import Http
    from twisted.web.resource import Resource
    from twisted.internet import reactor
    from twisted.web.server import Site

	# Home module    
    home = CorePost()
    
    @home.route("/")
    def home_root(request,**kwargs):
        return "HOME %s" % kwargs
    
    # First module
    module1 = CorePost('module1')
    
    @module1.route("/",Http.GET)
    def module1_get(request,**kwargs):
        return request.path
    
    @module1.route("/sub",Http.GET)
    def module1e_sub(request,**kwargs):
        return request.path
    
    # Second module
    module2 = CorePost('module2')
    
    @module2.route("/",Http.GET)
    def module2_get(request,**kwargs):
        return request.path
    
    @module2.route("/sub",Http.GET)
    def module2_sub(request,**kwargs):
        return request.path
    
    if __name__ == '__main__':
        app = Resource()
        app.putChild(home.path, home)
        app.putChild(module1.path,module1)
        app.putChild(module2.path,module2)
    
        factory = Site(app)
        reactor.listenTCP(8080, factory) 
        reactor.run()                   

The example above creates 3 modules ("/","module1","/module2") and exposes the following URLs:

	http://127.0.0.1:8080					
	http://127.0.0.1:8080/				
	http://127.0.0.1:8080/module1		
	http://127.0.0.1:8080/module1/			
	http://127.0.0.1:8080/module1/sub		
	http://127.0.0.1:8080/module2			
	http://127.0.0.1:8080/module2/			
	http://127.0.0.1:8080/module2/sub	

Path argument extraction
------------------------

CorePort can easily extract path arguments from an URL and convert them to the desired type.

The supported types are:

* *int*
* *float*
* *string*

Example:

	@app.route("/int/<int:intarg>/float/<float:floatarg>/string/<stringarg>",Http.GET)
	def test(request,intarg,floatarg,stringarg,**kwargs):
		pass
	    
Argument validation
-------------------

CorePost integrates the popular 'formencode' package to implement form and query argument validation.
Validators can be specified using a *formencode* Schema object, or via custom field-specific validators, e.g.:

	from corepost.web import CorePost, validate
	from corepost.enums import Http
	from formencode import Schema, validators
	
	app = CorePost()
	
	class TestSchema(Schema):
	    allow_extra_fields = True
	    childId = validators.Regex(regex="^value1|value2$")
		
	@app.route("/validate/<int:rootId>/schema",Http.POST)
	@validate(schema=TestSchema)
	def postValidateSchema(request,rootId,childId,**kwargs):
	    '''Validate using a common schema'''
	    return "%s - %s - %s" % (rootId,childId,kwargs)
	
	@app.route("/validate/<int:rootId>/custom",Http.POST)
	@validate(childId=validators.Regex(regex="^value1|value2$"))
	def postValidateCustom(request,rootId,childId,**kwargs):
	    '''Validate using argument-specific validators'
	    return "%s - %s - %s" % (rootId,childId,kwargs)	    

Please see the *FormEncode* <http://www.formencode.org/en/latest/Validator.html> documentation
for list of available validators:

* Common <http://www.formencode.org/en/latest/modules/validators.html#module-formencode.validators>
* National <http://www.formencode.org/en/latest/modules/national.html#module-formencode.national>
	    
@defer.inlineCallbacks support
------------------------------

If you want a deferred async method, just complete the request yourself, instead of returning a string response

	@app.route("/",Http.GET)
	@defer.inlineCallbacks
	def root(request,**kwargs):
		val = yield db.query("SELECT ....")
		request.write(val)
		request.finish()

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