Content types
=============

CorePost integrates support for JSON, YAML and XML (partially) based on request content types.

Parsing of incoming content
---------------------------

Based on the incoming content type in POST/PUT requests,
the body will be automatically parsed to JSON, YAML and XML (ElementTree)

* request.json
* request.yaml
* request.xml

and attached to the request::

	@route("/post/json",(Http.POST,Http.PUT))
	def test_json(self,request,**kwargs):
	    return "%s" % json.dumps(request.json)
	
	@route("/post/xml",(Http.POST,Http.PUT))
	def test_xml(self,request,**kwargs):
	    return "%s" % ElementTree.tostring(request.xml)
	
	@route("/post/yaml",(Http.POST,Http.PUT))
	def test_yaml(self,request,**kwargs):
	    return "%s" % yaml.dump(request.yaml)


Converting Python objects to expected content type
--------------------------------------------------

Instead of returning string responses, the code can just return Python objects.
Depending whether the caller can accept JSON (default) or YAML, the Python objects will be automatically converted::

    @route("/return/by/accept")
    def test_return_content_by_accepts(self,request,**kwargs):
        val = [{"test1":"Test1"},{"test2":"Test2"}]
        return val
        
Calling this URL with "Accept: application/json" will return:

::

	[{"test1": "Test1"}, {"test2": "Test2"}]
	
Calling it with "Accept: text/yaml" will return:

::

	- {test1: Test1}
	- {test2: Test2} 
	
