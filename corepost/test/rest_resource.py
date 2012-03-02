'''
Server tests
@author: jacekf
'''

from corepost import Response
from corepost.web import RestServiceContainer 

class DB():
    """Fake in-memory DB for testing"""
    customers = {}

class Customer():
    """Represents customer entity"""
    def __init__(self,customerId,firstName,lastName):
        (self.customerId,self.firstName,self.lastName) = (customerId,firstName,lastName)
        self.addresses = {}

class CustomerAddress():
    """Represents customer address entity"""
    def __init__(self,customer,streetNumber,streetName,stateCode,countryCode):
        (self.customer,self.streetNumber,self.streetName.self.stateCode,self.countryCode) = (customer,streetNumber,streetName,stateCode,countryCode)

class CustomerRestService():
    path = "/customer"
    
    def getAll(self,request):
        return DB.customers
    
    def get(self,request,customerId):
        return DB.customers[customerId] if customerId in DB.customers else Response(404, "Customer %s not found" % customerId)
    
    def post(self,request,customerId,firstName,lastName):
        if customerId in DB.customers:
            return Response(409,"Customer %s already exists" % customerId)
        else:
            DB.customers[customerId] = Customer(customerId, firstName, lastName)
            return Response(201)
        
    def put(self,request,customerId,firstName,lastName):
        if customerId in DB.customers:
            DB.customers[customerId].firstName = firstName
            DB.customers[customerId].lastName = lastName
            return Response(200)
        else:
            return Response(404, "Customer %s not found" % customerId)

    def delete(self,request,customerId):
        if customerId in DB.customers:
            del(DB.customers[customerId])
            return Response(200)
        else:
            return Response(404, "Customer %s not found" % customerId)
    
    def deleteAll(self,request):
        DB.customers.clear()
        return Response(200)

class CustomerAddressRestService():
    path = "/customer/<customerId>/address"
    
    def getAll(self,request,customerId):
        return DB.customers
    
    def get(self,request,customerId):
        return DB.customers[customerId] if customerId in DB.customers else Response(404, "Customer %s not found" % customerId)
    
    def post(self,request,customerId,firstName,lastName):
        if customerId in DB.customers:
            return Response(409,"Customer %s already exists" % customerId)
        else:
            DB.customers[customerId] = Customer(customerId, firstName, lastName)
            return Response(201)
        
    def put(self,request,customerId,firstName,lastName):
        if customerId in DB.customers:
            DB.customers[customerId].firstName = firstName
            DB.customers[customerId].lastName = lastName
            return Response(200)
        else:
            return Response(404, "Customer %s not found" % customerId)

    def delete(self,request,customerId):
        if customerId in DB.customers:
            del(DB.customers[customerId])
            return Response(200)
        else:
            return Response(404, "Customer %s not found" % customerId)
    
    def deleteAll(self,request):
        DB.customers.clear()
        return Response(200)


def run_rest_app():
    app = RestServiceContainer(restServices=(CustomerRestService(),))
    app.run(8085)
    
if __name__ == "__main__":
    run_rest_app()