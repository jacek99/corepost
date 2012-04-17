"""
Twisted REST micro-framework
================================

Based on *Flask* API, with plans for integrated multiprocessing support for full usage of all CPUs. 
Provides a more Flask/Sinatra-style API on top of the core *twisted.web* APIs.
Integrates FormEncode for path, form and query argument validation.

An example of a multi--module twisted.web CorePost REST application
which exposes two separate REST services (for a Customer and Customer Address entities):

::

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

And the BDD showing off its different features

https://github.com/jacek99/corepost/blob/master/corepost/test/feature/rest_app.feature

Links
`````

* `Website <http://github.com/jacek99/corepost>`_
* `Twisted <http://twistedmatrix.com>`_
* `FormEncode <http://www.formencode.org/>`_

Changelog
`````````
* 0.0.16:
    - minor bug fix for issue #4 (serializing object graphs to XML):
        https://github.com/jacek99/corepost/issues/3 
        As a result removed Jinja2 as a dependency, no longer needed by default
* 0.0.15:
    - minor bug fixes in auto-converting responses to JSON and parsing arguments/paths with unexpectec characters
* 0.0.14:
    - automatic parsing of query, form, JSON, YAML and XML arguments: 
      http://jacek99.github.com/corepost/argument_parsing.html
* 0.0.13:
    - perf fix to avoid unnecessary string concatenation when doing URL routing, after code review (thanks to Gerald Tremblay) 
* 0.0.12:
    - backwards incompatible change: added advanced URL routing for nested REST services.
      CorePost object is gone, REST services are now just standard classes.
      They get wrapped in a RESTResource object (see sample above) when exposed
* 0.0.11:
    - added support for request/response filters
* 0.0.10:
    - removed dependency on txZMQ which was not needed at this point (yet)
* 0.0.9:
     - fix for issue #3 (wrong class passes as 'self' to router method): 
         https://github.com/jacek99/corepost/issues/3 
* 0.0.8:
    - support for serializing of classes to JSON,XML,YAML based on caller's Accept header
    - separate routing functionality from CorePost Resource object, in preparation for future multicore support
* 0.0.7:
    - automatic parsing of incoming content (JSON, YAML, XML)
    - routing by incoming content type
    - automatic response conversion based on caller's Accept header (JSON/YAML
    - support for defer.returnValue() in @inlineCallbacks route methods
* 0.0.6 - redesigned API around classes and methods, rather than functions and global objects (after feedback from Twisted devs)
* 0.0.5 - added FormEncode validation for arguments
* 0.0.4 - path argument extraction, mandatory argument error checking

"""

from setuptools import setup

setup(
    name="CorePost",
    version="0.0.16",
    author="Jacek Furmankiewicz",
    author_email="jacek99@gmail.com",
    description=("A Twisted Web REST micro-framework"),
    license="BSD",
    keywords="twisted rest flask sinatra get post put delete web",
    url="https://github.com/jacek99/corepost",
    packages=['corepost', ],
    long_description=__doc__,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
         'twisted>=12.0.0',
         'formencode>=1.2.4',
         'pyyaml>=3.1.0'
    ],
    tests_require=[
         'httplib2>=0.7.1',
         'freshen>=0.2',
    ],
    zip_safe = True
)
