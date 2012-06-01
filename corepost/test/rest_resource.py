'''
Server tests
@author: jacekf
'''

from corepost import Response, NotFoundException, AlreadyExistsException
from corepost.web import RESTResource, route, Http 

from twisted.cred.portal import IRealm, Portal
from twisted.cred.checkers import FilePasswordDB
from twisted.web.static import File
from twisted.web.resource import IResource
from twisted.web.guard import HTTPAuthSessionWrapper, BasicCredentialFactory

from zope.interface import implements

# Security

# Database
class DB():
    """Fake in-memory DB for testing"""
    customers = {}

    @classmethod
    def getAllCustomers(cls):
        return DB.customers.values()

    @classmethod
    def getCustomer(cls,customerId):
        if customerId in DB.customers:
            return DB.customers[customerId]
        else:
            raise NotFoundException("Customer",customerId)

    @classmethod
    def saveCustomer(cls,customer):
        if customer.customerId in DB.customers:
            raise AlreadyExistsException("Customer",customer.customerId)
        else:
            DB.customers[customer.customerId] = customer

    @classmethod
    def deleteCustomer(cls,customerId):
        if customerId in DB.customers:
            del(DB.customers[customerId])
        else:
            raise NotFoundException("Customer",customerId)

    @classmethod
    def deleteAllCustomers(cls):
        DB.customers.clear()

    @classmethod
    def getCustomerAddress(cls,customerId,addressId):
        c = DB.getCustomer(customerId)
        if addressId in c.addresses:
            return c.addresses[addressId]
        else:
            raise NotFoundException("Customer Address",addressId)


class Customer:
    """Represents customer entity"""
    def __init__(self,customerId,firstName,lastName):
        (self.customerId,self.firstName,self.lastName) = (customerId,firstName,lastName)
        self.addresses = {}

class CustomerAddress:
    """Represents customer address entity"""
    def __init__(self,streetNumber,streetName,stateCode,countryCode):
        (self.streetNumber,self.streetName,self.stateCode,self.countryCode) = (streetNumber,streetName,stateCode,countryCode)

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
    app.run(8085)
    
if __name__ == "__main__":
    run_rest_app()