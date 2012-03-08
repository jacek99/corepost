Asynchronous Operations
=================

@defer.inlineCallbacks support
-----------------------

If you want a deferred async method, just use *defer.returnValue()*::

	@route("/",Http.GET)
	@defer.inlineCallbacks
	def root(self,request,**kwargs):
		val1 = yield db.query("SELECT ....")
		val2 = yield db.query("SELECT ....")
		defer.returnValue(val1 + val2)

This is standard Twisted functionality.
	
