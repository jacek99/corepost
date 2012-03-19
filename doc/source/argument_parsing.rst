Argument parsing
===================

CorePost can automatically parse query arguments, form arguments, as well as basic JSON, YAML and XML documents
and extract those as direct arguments to a REST router method.

Let's say we have a basic method that responds to GET, POST and PUT requests.
It expects a first name and last name and outputs them back in the response::

	@router("/name",(Http.GET,Http.POST,Http.PUT))
	def getName(self,request,first,last,**kwargs):
		return "%s %s" % (first, last)
		
Query arguments
---------------

For GET requests, the query arguments will be automatically parsed, e.g.::

	curl http://127.0.0.1/name?first=John&last=Doe

Form encoded arguments
----------------------

For POST/PUT requests, any form-encoded arguments will be automatically parsed, e.g.::

	curl -X POST http://localhost/name -d "first=John&last=Doe"

JSON document arguments
-----------------------

For the same method, you could just post a JSON document instead that looks like this::

	{"first":"John","last":"Doe"}
	
CorePost will automatically pass all the root elements of the document as arguments into a method.
Requires the *'application/json'* content type to be passed.

YAML document arguments
-----------------------

For the same method, you could just post a YAML document that looks like this::

	first:John
	last:Doe
	
CorePost will automatically pass all the root elements of the document as arguments into a method.
Requires the *'text/yaml'* content type to be passed.

XML document arguments
----------------------

XML documents are supported as well. In that case, CorePost will first parse all the attributes on the root node
and then all of the children underneath the main root node.

Hence all of the XML formats below are valid and would generate the same parameters to a method.

Attributes only::

	<root first="John" last="Doe"/>
	
Mix of attributes and child nodes::	
	
	<root first="John">
		<last>Doe</last>
	</root>
	
Child nodes only::

	<root>
		<first>John</first> 
		<last>Doe</last>
	</root>

Requires the *'text/xml'* OR *'application/xml'* content type to be passed.
	
As you can see from the examples above, a single CorePost router method can handle all these varied forms of argument parsing
for you without any additional effort.
	
	
