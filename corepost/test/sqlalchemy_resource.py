'''
SQL Alchemy example application
@author: jacekf
'''

from corepost import Response, NotFoundException, AlreadyExistsException
from corepost.web import RESTResource, route, Http 

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref, Session

# support different sessions for read/writes for master/read slave configuration
class WriteSession(Session):
    """SQL Alchemy session for writes (to master)"""
    def __init__(self):
        Session.__init__(self)

class ReadSession(Session):
    """SQL Alchemy session for reads (from read slaves)"""
    def __init__(self):
        Session.__init__(self)

# SQL Alchemy entities
Base = declarative_base()

class Customer(Base):
    """Represents customer entity"""
    __tablename__ = "customer"

    customerId = Column("customer_id",Integer,primary_key=True)
    firstName = Column("first_name",String(50))
    middleName = Column("middle_name",String(50),nullable=True)
    lastName = Column("last_name",String(50))
    
    def __init__(self,customerId,firstName,middleName,lastName):
        (self.customerId,self.firstName,self.middleName,self.lastName) = (customerId,firstName,middleName,lastName)

class CustomerAddress(Base):
    """Represents customer address entity"""
    addressId = Column("address_id",Integer,primary_key=True)
    addressLine1 = Column("address_line1",String(255))
    addressLine2 = Column("address_line2",String(255),nullable=True)
    city = Column("city",String(50))
    stateCode = Column("state_code",String(2))
    countryCode = Column("country_code",String(2))
    
    def __init__(self,addressLine1,addressLine2,city,stateCode,countryCode):
        (self.addressLine1,self.addressLine2,self.city,self.stateCode,self.countryCode) = (addressLine1,addressLine2,city,stateCode,countryCode)

class CustomerDAO:
    """SQLAlchemy DAO that uses blocking I/O. Needs to always be run in defer.deferToThread()"""
    
    def findById(self,customerId):
        pass
    
    def save(self,customer):
        pass
    
    def merge(self,customer):
        pass
    
    def delete(self,customer):
        pass    

# REST services

class CustomerREST:
    """Customer REST service"""
    path = "/customer"
    
    @route("/",Http.GET)
    def getAll(self,request,**kwargs):
        pass

    @route("/<customerId>",Http.GET)
    def get(self,request,customerId,**kwargs):
        pass

    @route("/",Http.POST)
    def post(self,request,customerId,firstName,middleName=None,lastName,**kwargs):
        pass

    @route("/<customerId>",Http.PUT)
    def put(self,request,customerId,firstName=None,middleName=None,lastName=None,**kwargs):
        pass

    @route("/<customerId>",Http.DELETE)
    def delete(self,request,customerId,**kwargs):
        pass

class CustomerAddressREST:
    """Customer Address REST service"""
    path = "/customer/<customerId>/address"
    
    @route("/",Http.GET)
    def getAll(self,request,**kwargs):
        pass

    @route("/<addressId>",Http.GET)
    def get(self,request,customerId,addressId,**kwargs):
        pass

    @route("/",Http.POST)
    def post(self,request,customerId,addressId,addressLine1,addressLine2=None,city,stateCode,countryCode,**kwargs):
        pass

    @route("/<addressId>",Http.PUT)
    def put(self,request,customerId,self,request,customerId,addressId,addressLine1=None,addressLine2=None,city=None,stateCode=None,countryCode=None,**kwargs):
        pass

    @route("/<addressId>",Http.DELETE)
    def delete(self,request,customerId,addressId,**kwargs):
        pass


def run_sqlalchemy_app():
    app = RESTResource((CustomerREST(),CustomerAddressREST()))
    app.run(8086)
    pass
    
if __name__ == "__main__":
    run_sqlalchemy_app()