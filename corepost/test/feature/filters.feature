Using step definitions from: '../steps'

@filters
Feature: Filters
	CorePost should be able to
	filter incoming requests and outgoing responses

	Background:
		Given 'filter_resource' is running

	Scenario: Filter turns 404 into 503
		When as user 'None:None' I GET 'http://127.0.0.1:8083/wrongurl'
		Then I expect HTTP code 503

	Scenario: Request filter adds a header + wrap around requests
		When I prepare HTTP header 'Accept' = 'application/json'
		When as user 'None:None' I GET 'http://127.0.0.1:8083/'
		Then I expect HTTP code 200
		# 'custom-header' should be added
		# 'x-wrap-input' should be added from wrap request filter
		And I expect JSON content
		"""
{
    "accept": "application/json", 
    "accept-encoding": "gzip, deflate", 
    "custom-header": "Custom Header Value", 
    "host": "127.0.0.1:8083", 
    "x-wrap-input": "Input"
}
		"""
		# 'x-wrap-header' should be added from wrap response filter
		And I expect 'x-wrap-output' header matches 'Output'
		