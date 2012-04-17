Using step definitions from: '../steps'

@rest
Feature: REST App
	CorePost should be able to build REST applications
	for nested REST resources

	Background:
		Given 'rest_resource' is running
		# make sure it is empty
		When as user 'None:None' I DELETE 'http://127.0.0.1:8085/customer'
		Then I expect HTTP code 200
		# add a few default customers
		When as user 'None:None' I POST 'http://127.0.0.1:8085/customer' with 'customerId=d1&firstName=John&lastName=Doe1'
		Then I expect HTTP code 201
		When as user 'None:None' I POST 'http://127.0.0.1:8085/customer' with 'customerId=d2&firstName=John&lastName=Doe2'
		Then I expect HTTP code 201
		When as user 'None:None' I POST 'http://127.0.0.1:8085/customer' with 'customerId=d3&firstName=John&lastName=Doe3'
		Then I expect HTTP code 201

	
	@customer
	Scenario: Full Customer lifecycle
		When as user 'None:None' I GET 'http://127.0.0.1:8085/customer'
		Then I expect HTTP code 200
		And I expect JSON content
		"""
[
    {
        "addresses": {}, 
        "customerId": "d2", 
        "firstName": "John", 
        "lastName": "Doe2"
    }, 
    {
        "addresses": {}, 
        "customerId": "d3", 
        "firstName": "John", 
        "lastName": "Doe3"
    }, 
    {
        "addresses": {}, 
        "customerId": "d1", 
        "firstName": "John", 
        "lastName": "Doe1"
    }
]
		"""
		# add 1
		When as user 'None:None' I POST 'http://127.0.0.1:8085/customer' with 'customerId=c1&firstName=John&lastName=Doe'
		Then I expect HTTP code 201
		When as user 'None:None' I GET 'http://127.0.0.1:8085/customer/c1'
		Then I expect HTTP code 200
		And I expect JSON content
		"""
{
    "addresses": {}, 
    "customerId": "c1", 
    "firstName": "John", 
    "lastName": "Doe"
}
		"""
		# update
		When as user 'None:None' I PUT 'http://127.0.0.1:8085/customer/c1' with 'firstName=Jill&lastName=Jones'
		Then I expect HTTP code 200
		When as user 'None:None' I GET 'http://127.0.0.1:8085/customer/c1'
		Then I expect HTTP code 200
		And I expect JSON content
		"""
{
    "addresses": {}, 
    "customerId": "c1", 
    "firstName": "Jill", 
    "lastName": "Jones"
}
		"""	
		# delete
		When as user 'None:None' I DELETE 'http://127.0.0.1:8085/customer/c1'
		Then I expect HTTP code 200
		When as user 'None:None' I GET 'http://127.0.0.1:8085/customer/c1'
		Then I expect HTTP code 404
		# delete all
		When as user 'None:None' I DELETE 'http://127.0.0.1:8085/customer'
		Then I expect HTTP code 200
		When as user 'None:None' I GET 'http://127.0.0.1:8085/customer'
		Then I expect HTTP code 200
		And I expect JSON content
		"""
		[]
		"""
		
	@customer_address
	Scenario: Full Customer Address lifecycle
		When as user 'None:None' I GET 'http://127.0.0.1:8085/customer/d1/address'
		Then I expect HTTP code 200
		And I expect JSON content
		"""
		{}
		"""
		# add 1
		When as user 'None:None' I POST 'http://127.0.0.1:8085/customer/d1/address' with 'addressId=HOME&streetNumber=100&streetName=MyStreet&stateCode=CA&countryCode=US'
		Then I expect HTTP code 201
		# get just the address
		When as user 'None:None' I GET 'http://127.0.0.1:8085/customer/d1/address/HOME'
		Then I expect HTTP code 200
		And I expect JSON content
		"""
{
    "countryCode": "US", 
    "stateCode": "CA", 
    "streetName": "MyStreet", 
    "streetNumber": "100"
}
		"""
		# get the customer with the address
		When as user 'None:None' I GET 'http://127.0.0.1:8085/customer/d1'
		Then I expect HTTP code 200
		And I expect JSON content
		"""
{
    "addresses": {
        "HOME": {
            "countryCode": "US", 
            "stateCode": "CA", 
            "streetName": "MyStreet", 
            "streetNumber": "100"
        }
    }, 
    "customerId": "d1", 
    "firstName": "John", 
    "lastName": "Doe1"
}
       	"""
		# update address
		When as user 'None:None' I PUT 'http://127.0.0.1:8085/customer/d1/address/HOME' with 'streetNumber=1002&streetName=MyStreet2&stateCode=CA&countryCode=US'
		Then I expect HTTP code 200
		When as user 'None:None' I GET 'http://127.0.0.1:8085/customer/d1/address/HOME'
		Then I expect HTTP code 200
		And I expect JSON content
		"""
{
    "countryCode": "US", 
    "stateCode": "CA", 
    "streetName": "MyStreet2", 
    "streetNumber": "1002"
}
		"""
		# delete address
		When as user 'None:None' I DELETE 'http://127.0.0.1:8085/customer/d1/address/HOME'
		Then I expect HTTP code 200
		When as user 'None:None' I GET 'http://127.0.0.1:8085/customer/d1/address/HOME'
		Then I expect HTTP code 404
		
	@customer @xml @issue4
	Scenario: Customers as XML (Issue #4)
		# all
		When I prepare HTTP header 'Accept' = 'application/xml'
		When as user 'None:None' I GET 'http://127.0.0.1:8085/customer'
		Then I expect HTTP code 200
		Then I expect content contains '<list><item><lastName>Doe2</lastName><customerId>d2</customerId><firstName>John</firstName><addresses></addresses></item><item><lastName>Doe3</lastName><customerId>d3</customerId><firstName>John</firstName><addresses></addresses></item><item><lastName>Doe1</lastName><customerId>d1</customerId><firstName>John</firstName><addresses></addresses></item></list>'
		# 1
		When I prepare HTTP header 'Accept' = 'application/xml'
		When as user 'None:None' I GET 'http://127.0.0.1:8085/customer/d2'
		Then I expect HTTP code 200
		Then I expect content contains '<item><lastName>Doe2</lastName><customerId>d2</customerId><firstName>John</firstName><addresses></addresses></item>'
		# 1 with address
		When as user 'None:None' I POST 'http://127.0.0.1:8085/customer/d2/address' with 'addressId=HOME&streetNumber=100&streetName=MyStreet&stateCode=CA&countryCode=US'
		When I prepare HTTP header 'Accept' = 'application/xml'
		When as user 'None:None' I GET 'http://127.0.0.1:8085/customer/d2'
		Then I expect HTTP code 200
		Then I expect content contains '<item><lastName>Doe2</lastName><customerId>d2</customerId><firstName>John</firstName><addresses><HOME><countryCode>US</countryCode><streetName>MyStreet</streetName><streetNumber>100</streetNumber><stateCode>CA</stateCode></HOME></addresses></item>'
		