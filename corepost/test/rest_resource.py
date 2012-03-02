'''
Server tests
@author: jacekf
'''

from corepost import Response, NotFoundException, AlreadyExistsException
from corepost.web import RESTResource, route, Http 
from twisted.python import log
import sys

#log.startLogging(sys.stdout)

class DB():
    """Fake in-memory DB for testing"""
    customers = {}

class Customer():
    """Represents customer entity"""
    def __init__(self,customerId,firstName,lastName):
        (self.customerId,self.firstName,self.lastName) = (customerId,firstName,lastName)
        self.addresses = []

class CustomerAddress():
    """Represents customer address entity"""
    def __init__(self,customer,streetNumber,streetName,stateCode,countryCode):
        (self.customer,self.streetNumber,self.streetName.self.stateCode,self.countryCode) = (customer,streetNumber,streetName,stateCode,countryCode)

class CustomerRestService():
    path = "/customer"

    @route("/")
    def getAll(self,request):
        return DB.customers.values()
    
    @route("/<customerId>")
    def get(self,request,customerId):
        if customerId in DB.customers:
            return DB.customers[customerId]
        else:
            raise NotFoundException("Customer", customerId)
    
    @route("/",Http.POST)
    def post(self,request,customerId,firstName,lastName):
        if customerId in DB.customers:
            raise AlreadyExistsException("Customer",customerId)
        else:
            DB.customers[customerId] = Customer(customerId, firstName, lastName)
            return Response(201)
    
    @route("/<customerId>",Http.PUT)        
    def put(self,request,customerId,firstName,lastName):
        if customerId in DB.customers:
            DB.customers[customerId].firstName = firstName
            DB.customers[customerId].lastName = lastName
            return Response(200)
        else:
            raise NotFoundException("Customer", customerId)

    @route("/<customerId>",Http.DELETE)
    def delete(self,request,customerId):
        if customerId in DB.customers:
            del(DB.customers[customerId])
            return Response(200)
        else:
            raise NotFoundException("Customer", customerId)
    
    @route("/",Http.DELETE)
    def deleteAll(self,request):
        DB.customers.clear()
        return Response(200)

def run_rest_app():
    app = RESTResource((CustomerRestService(),))
    app.run(8085)
    
if __name__ == "__main__":
    run_rest_app()