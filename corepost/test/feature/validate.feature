Using step definitions from: '../steps'

@validate
Feature: Argument Validators
	CorePost should be able to correctly validate path, query and form arguments
	
	@validate
	Scenario Outline: Form argument validation
		Given 'arguments' is running
		# childId accepts only jacekf or test, via Regex validator
		When as user 'None:None' I POST 'http://127.0.0.1:8082/validate/23/<url>' with '<args>'
		Then I expect HTTP code <code>
		And I expect content contains '<content>'

		Examples:
			| url		| args												| code	| content																|
			# validates using argument-specific validators
			| custom	| childId=jacekf									| 201	| 23 - jacekf - {}														|
			| custom	| childId=jacekf&otherId=test						| 201	| 23 - jacekf - {'otherId': 'test'}										|
			| custom	| childId=test										| 201	| 23 - test - {}														|
			| custom	| childId=wrong										| 400	| childId: The input is not valid ('wrong')								|			
			# validates using Schema
			| schema	| childId=jacekf									| 201	| 23 - jacekf - {}														|
			| schema	| childId=jacekf&otherId=test						| 201	| 23 - jacekf - {'otherId': 'test'}										|
			| schema	| childId=test										| 201	| 23 - test - {}														|
			| schema	| childId=wrong										| 400	| childId: The input is not valid ('wrong')								|			
		