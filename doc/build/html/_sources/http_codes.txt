HTTP codes
==========

By default, CorePost returns the appropriate HTTP code based on the HTTP method:

Success:

* 200 (OK) - GET, DELETE, PUT
* 201 (Created) - POST
	
Errors:

* 404 - not able to match any URL.
* 400 - missing mandatory argument (driven from the arguments on the actual functions)
* 400 - argument failed validation
* 500 - server error
	
