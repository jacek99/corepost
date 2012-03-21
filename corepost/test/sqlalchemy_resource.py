'''
SQL Alchemy example application
@author: jacekf
'''

from corepost import Response, NotFoundException, AlreadyExistsException
from corepost.web import RESTResource, route, Http 

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

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

def run_sqlalchemy_app():
    app = RESTResource((CustomerRESTService(),CustomerAddressRESTService()))
    app.run(8086)
    
if __name__ == "__main__":
    run_rest_app()