URL Routing
=================

@route decorator
----------------

Via a simple *@route* decorator you can automatically route *twisted.web* Request objects to your class method
based on URL (with dynamic paths), HTTP method, expected content type, etc::

    from corepost.web import route, RESTResource
    from corepost.enums import Http
    
    class RESTService():
    
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
        app = RESTResource((RESTService(),))
        app.run()

*Note*:

	This piece of code::
	
	        app.run()
	        
	is just for convenience when showing code samples and writing unit tests. 
	In a real production application you would use existing Twisted *twistd* functionality:
	
	* http://twistedmatrix.com/documents/current/core/howto/basics.html
	* http://twistedmatrix.com/documents/current/core/howto/application.html
	* http://twistedmatrix.com/documents/current/core/howto/tap.html

Path argument extraction
------------------------

CorePort can easily extract path arguments from an URL and convert them to the desired type.

The supported types are:

* *int*
* *float*
* *string*

Example::

	@route("/int/<int:intarg>/float/<float:floatarg>/string/<stringarg>",Http.GET)
	def test(self,request,intarg,floatarg,stringarg,**kwargs):
		pass

Routing requests by incoming content type
-----------------------------------------

Based on the incoming content type in POST/PUT requests, the *same* URL can be hooked up to different router methods::

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
