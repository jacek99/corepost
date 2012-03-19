Argument validation
===================

CorePost integrates the popular 'formencode' package to implement form and query argument validation.
Validators can be specified using a *formencode* Schema object, or via custom field-specific validators.

Example::

	from corepost.web import validate, route
	from corepost.enums import Http
	from formencode import Schema, validators
	
	class TestSchema(Schema):
	    allow_extra_fields = True
	    childId = validators.Regex(regex="^value1|value2$")
	
	class MyApp():
		
		@route("/validate/<int:rootId>/schema",Http.POST)
		@validate(schema=TestSchema())
		def postValidateSchema(self,request,rootId,childId,**kwargs):
		    '''Validate using a common schema'''
		    return "%s - %s - %s" % (rootId,childId,kwargs)
		
		@route("/validate/<int:rootId>/custom",Http.POST)
		@validate(childId=validators.Regex(regex="^value1|value2$"))
		def postValidateCustom(self,request,rootId,childId,**kwargs):
		    '''Validate using argument-specific validators'''
		    return "%s - %s - %s" % (rootId,childId,kwargs)	    


Please see the *FormEncode* documentation:

http://www.formencode.org/en/latest/Validator.html

for list of available validators:

* Common : http://www.formencode.org/en/latest/modules/validators.html#module-formencode.validators
* National : http://www.formencode.org/en/latest/modules/national.html#module-formencode.national


