Twisted REST micro-framework
================================

Based on *Flask* API, with integrated multiprocessing support for full usage of all CPUs. 
Provides a more Flask/Sinatra-style API on top of the core *twisted.web* APIs.

Geared towards creating REST-oriented server platforms (e.g. as a source of data for a Javascript MVC app).
Tested exclusively on PyPy for maximum performance.

Example:
^^^^^^^

	from corepost.server import CorePost
	from corepost.enums import Http
	
	app = CorePost()
	
	@app.route("/",Http.GET)
	def root(request):
	    return request.path
	
	@app.route("/test",Http.GET)
	def test(request):
	    return request.path
	
	@app.route("/test/<int:numericid>/test2/<stringid>",Http.GET)
	def test_get_resources(request,numericid,stringid,**kwargs):
	    return "%s - %s" % (numericid,stringid)
	
	if __name__ == '__main__':
	    app.run()
	    
Performance
^^^^^^^^^^^

Pushing 8,000+ TPS on a simple 'Hello World' app using 'ab -n 100000 -c 200' 
for benchmarking while running on PyPy 1.6

Plans
^^^^^

* match all the relevant features of the Flask API
* integrate twisted.internet.processes in order to scale to multiple CPU cores : http://pypi.python.org/pypi/twisted.internet.processes