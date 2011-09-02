Using step definitions from: '../steps'

@validate
Feature: Argument Validators
	CorePost should be able to correctly validate path, query and form arguments
	
	@validate
	Scenario Outline: Path argument extraction
		Given 'arguments' is running
		When as user 'None:None' I POST 'http://127.0.0.1:8082/validate/23/children' with '<args>'
		Then I expect HTTP code <code>
		And I expect content contains '<content>'

		Examples:
			| args												| code	| content																|
			| childId=jacekf									| 201	| 23 - jacekf - {}														|
			| childId=jacekf&otherId=test						| 201	| 23 - jacekf - {'otherId': 'test'}										|
		