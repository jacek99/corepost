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

	    
@defer.inlineCallbacks support
------------------------------

If you want a deferred async method, just complete the request yourself, instead of returning a string response

	@app.route("/",Http.GET)
	@defer.inlineCallbacks
	def root(request,**kwargs):
		val = yield db.query("SELECT ....")
		request.write(val)
		request.finish()
	    	        
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