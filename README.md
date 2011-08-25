Twisted REST micro-framework
================================

Based on *Flask* API, with integrated multiprocessing support for full usage of all CPUs. 
Provides a more Flask/Sinatra-style API on top of the core *twisted.web* APIs.

Geared towards creating REST-oriented server platforms (e.g. as a source of data for a Javascript MVC app).
Tested exclusively on PyPy for maximum performance.

Example
-------

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
	    app.run()
	    
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

Plans
-----

* match all the relevant features of the Flask API
* integrate twisted.internet.processes in order to scale to multiple CPU cores : http://pypi.python.org/pypi/twisted.internet.processes