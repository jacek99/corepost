Modular REST applications
=========================

A typical case in REST is where you have parent/child resources (business entities), e.g.

::

	Customer
	
		Customer Address
		
		Customer Phone
		
		Customer Order
		
			Customer Invoice
			
				Customer Invoice Payment

etc.

This can create a URL structure like:

::

	/customer
	
	/customer/<customerId>
	
	/customer/<customerId>/address
	
	/customer/<customerId>/address/<addressId>
	
	/customer/<customerId>/phone
	
	/customer/<customerId>/phone/<phoneId>
	
	/customer/<customerId>/invoice
	
	/customer/<customerId>/invoice/<invoiceId>
	
	/customer/<customerId>/invoice/<invoiceId>/payment
	
	/customer/<customerId>/invoice/<invoiceId>/payment/<paymentId>
	

CorePost allows you to write small, modular classes that implement a REST service for just a single entity,
driven by URL paths with dynamic elements in them (e.g. the *customerId*, *invoiceId*, *paymentId* path parameters in the sample above).
You do not have to mesh all these different entities in a single class.

At the end, you wrap all of the different REST services in a single *RESTResource* object (which extends the regular Twisted Web Resource object)
and it takes care of routing the request to the appropriate class.

Here is a full-blown example of two REST services for Customer and Customer Address::

	from corepost import Response, NotFoundException, AlreadyExistsException
	from corepost.web import RESTResource, route, Http 

	class CustomerRESTService():
	    path = "/customer"
	
	    @route("/")
	    def getAll(self,request):
	        return DB.getAllCustomers()
	    
	    @route("/<customerId>")
	    def get(self,request,customerId):
	        return DB.getCustomer(customerId)
	    
	    @route("/",Http.POST)
	    def post(self,request,customerId,firstName,lastName):
	        customer = Customer(customerId, firstName, lastName)
	        DB.saveCustomer(customer)
	        return Response(201)
	    
	    @route("/<customerId>",Http.PUT)        
	    def put(self,request,customerId,firstName,lastName):
	        c = DB.getCustomer(customerId)
	        (c.firstName,c.lastName) = (firstName,lastName)
	        return Response(200)
	
	    @route("/<customerId>",Http.DELETE)
	    def delete(self,request,customerId):
	        DB.deleteCustomer(customerId)
	        return Response(200)
	    
	    @route("/",Http.DELETE)
	    def deleteAll(self,request):
	        DB.deleteAllCustomers()
	        return Response(200)
	
	class CustomerAddressRESTService():
	    path = "/customer/<customerId>/address"
	
	    @route("/")
	    def getAll(self,request,customerId):
	        return DB.getCustomer(customerId).addresses
	    
	    @route("/<addressId>")
	    def get(self,request,customerId,addressId):
	        return DB.getCustomerAddress(customerId, addressId)
	    
	    @route("/",Http.POST)
	    def post(self,request,customerId,addressId,streetNumber,streetName,stateCode,countryCode):
	        c = DB.getCustomer(customerId)
	        address = CustomerAddress(streetNumber,streetName,stateCode,countryCode)
	        c.addresses[addressId] = address
	        return Response(201)
	    
	    @route("/<addressId>",Http.PUT)        
	    def put(self,request,customerId,addressId,streetNumber,streetName,stateCode,countryCode):
	        address = DB.getCustomerAddress(customerId, addressId)
	        (address.streetNumber,address.streetName,address.stateCode,address.countryCode) = (streetNumber,streetName,stateCode,countryCode)
	        return Response(200)
	
	    @route("/<addressId>",Http.DELETE)
	    def delete(self,request,customerId,addressId):
	        DB.getCustomerAddress(customerId, addressId) #validate address exists
	        del(DB.getCustomer(customerId).addresses[addressId])
	        return Response(200)
	    
	    @route("/",Http.DELETE)
	    def deleteAll(self,request,customerId):
	        c = DB.getCustomer(customerId)
	        c.addresses = {}
	        return Response(200)
	
	
	def run_rest_app():
	    app = RESTResource((CustomerRESTService(),CustomerAddressRESTService()))
	    app.run(8080)
	    
	if __name__ == "__main__":
	    run_rest_app()
	
