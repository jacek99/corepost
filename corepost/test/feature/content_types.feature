Using step definitions from: '../steps'

@content_types
Feature: Content types
	CorePost should be able to
	correctly parse/generate
	JSON/XML/YAML based on content types

	@json
	Scenario Outline: Parse incoming JSON data
		Given 'home_resource' is running
		When as user 'None:None' I <method> 'http://127.0.0.1:8080/post/json' with JSON
		"""
		{"test":"test2"}
		"""
		Then I expect HTTP code <code>
		And I expect JSON content
		"""
		{"test":"test2"}
		"""
		
		Examples:
			| method	| code	|
			| POST		| 201	|
			| PUT		| 200	|

	@xml
	Scenario Outline: Parse incoming XML data
		Given 'home_resource' is running
		When as user 'None:None' I <method> 'http://127.0.0.1:8080/post/xml' with XML
		"""
		<root><test>TEST</test><test2>Yo</test2></root>
		"""
		Then I expect HTTP code <code>
		# ElementTree object
		And I expect content contains '<Element 'root' at'
		
		Examples:
			| method	| code	|
			| POST		| 201	|
			| PUT		| 200	|
			
			