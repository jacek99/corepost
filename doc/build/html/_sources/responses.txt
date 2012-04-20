Returning responses
===================

There are a number of ways in which you can return a response from a REST service

String
------

You can simply return a plain text String. CorePost will return the appropriate HTTP code for you::

	    @route("/",Http.GET)
	    def root(self,request,**kwargs):
	        return "Hello"

Dictionaries, lists or classes
------------------------------

You can return straight dictionaries:: 

	    @route("/",Http.GET)
	    def root(self,request,**kwargs):
	        return {"test":"test"}

or lists::

	    @route("/",Http.GET)
	    def root(self,request,**kwargs):
	        return [{"test":"test"},{"test":"test2"}]

or classes::

	    @route("/",Http.GET)
	    def root(self,request,**kwargs):
	        return SomeClass()

CorePost will serialize each of them to the appropriate content type (JSON,YAML or XML), depending on what the caller can accept.

Response objects
----------------

This option gives you the most control, as you can explicitly specify the response content, headers and HTTP code.
You need to return an instance of *corepost.Response* object::

	class Response:
	    """
	    Custom response object, can be returned instead of raw string response
	    """
	    def __init__(self,code=200,entity=None,headers={}):
	    	pass

Example::

    @route("/",Http.POST)
    def post(self,request,customerId,addressId,streetNumber,streetName,stateCode,countryCode):
        c = DB.getCustomer(customerId)
        address = CustomerAddress(streetNumber,streetName,stateCode,countryCode)
        c.addresses[addressId] = address
        return Response(201)
