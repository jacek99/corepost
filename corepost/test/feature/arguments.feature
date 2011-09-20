Using step definitions from: '../steps'

@arguments
Feature: Arguments
	CorePost should be able to correctly extract arguments
	from paths, query arguments and form arguments
	
	@arguments_ok
	Scenario Outline: Path argument extraction
		Given 'arguments' is running
		When as user 'None:None' I GET 'http://127.0.0.1:8082<url>'
		Then I expect HTTP code <code>
		And I expect content contains '<content>'

		Examples:
			| url												| code	| content																|
			| /int/1/float/1.1/string/TEST						| 200	| [(<type 'int'>, 1), (<type 'float'>, 1.1), (<type 'str'>, 'TEST')]	|
			| /int/1/float/1/string/TEST						| 200	| [(<type 'int'>, 1), (<type 'float'>, 1.0), (<type 'str'>, 'TEST')]	|
			| /int/1/float/1/string/23							| 200	| [(<type 'int'>, 1), (<type 'float'>, 1.0), (<type 'str'>, '23')]	|
						
	@arguments_error
	Scenario Outline: Path argument extraction - error handling
		Given 'arguments' is running
		When as user 'None:None' I GET 'http://127.0.0.1:8082<url>'
		Then I expect HTTP code <code>
		And I expect content contains '<content>'

		Examples:
			| url												| code	| content																|
			| /int/WRONG/float/1.1/string/TEST					| 404	| URL '/int/WRONG/float/1.1/string/TEST' not found						|
			| /int/1/float/WRONG/string/TEST					| 404	| URL '/int/1/float/WRONG/string/TEST' not found						|
											|