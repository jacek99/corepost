'''
Created on 2012-04-17

@author: jacekf
'''
from corepost.web import route
from twisted.python.constants import NamedConstant, Names

class REST_METHOD(Names):
    GET_ALL = NamedConstant()
    GET_ONE = NamedConstant()
    POST = NamedConstant()
    PUT = NamedConstant()
    DELETE = NamedConstant()
    DELETE_ALL = NamedConstant()
    ALL = NamedConstant()

class DatabaseRegistry:

    __registry = {}

    @classmethod
    def getConnection(cls,name=None):
        return DatabaseRegistry.__registery[name]
    
    @classmethod
    def registerPool(cls,name,dbPool):
        """Registers a DB connection pool under an appropriate name"""
        DatabaseRegistry.__registry[name] = dbPool
        
    @classmethod
    def getManager(cls,name=None,queriesFile=None):
        """Returns the high-level SQL data manager for easy SQL manipulation"""
        pass

class SqlDataManager:
    
    def __init__(self,table,columnMapping={}):
        pass    
    
class CustomerSqlService:
    path = "/customer"
    entityId ="<customerId>"
    dataManager = DatabaseRegistry.getManager("customer")
    methods = (REST_METHOD.GET_ONE,REST_METHOD.POST,REST_METHOD.PUT,REST_METHOD.DELETE)

class CustomerAddressSqlService:
    path = "/customer/<customerId>/address"
    entityId = "<addressId>"
    dataManager = DatabaseRegistry.getManager("customer_address")
    methods = (REST_METHOD.ALL,)
    
