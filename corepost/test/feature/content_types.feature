Using step definitions from: '../steps'

@content_types
Feature: Content types
	CorePost should be able to
	correctly parse/generate
	JSON/XML/YAML based on content types

	Background:
		Given 'home_resource' is running

	@json
	Scenario Outline: Parse incoming JSON data
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

	@json
	Scenario Outline: Handle invalid incoming JSON data
		When as user 'None:None' I <method> 'http://127.0.0.1:8080/post/json' with JSON
		"""
		wrong_json
		"""
		Then I expect HTTP code 400
		And I expect content contains 'Unable to parse JSON body: No JSON object could be decoded'
		
		Examples:
			| method	| 
			| POST		| 
			| PUT		| 

	@xml
	Scenario Outline: Parse incoming XML data
		When as user 'None:None' I <method> 'http://127.0.0.1:8080/post/xml' with XML
		"""
		<root><test>TEST</test><test2>Yo</test2></root>
		"""
		Then I expect HTTP code <code>
		# ElementTree object
		And I expect content contains '<root><test>TEST</test><test2>Yo</test2></root>'
		
		Examples:
			| method	| code	|
			| POST		| 201	|
			| PUT		| 200	|

	@xml
	Scenario Outline: Handle invalid XML data
		When as user 'None:None' I <method> 'http://127.0.0.1:8080/post/xml' with XML
		"""
		wrong xml
		"""
		Then I expect HTTP code 400
		And I expect content contains 'Unable to parse XML body: syntax error: line 1, column 0'
		
		Examples:
			| method	| 
			| POST		| 
			| PUT		| 

			
	@yaml
	Scenario Outline: Parse incoming YAML data
		When as user 'None:None' I <method> 'http://127.0.0.1:8080/post/yaml' with YAML
		"""
invoice: 34843
date   : 2001-01-23
bill-to: &id001
    given  : Chris
    family : Dumars
    address:
        lines: |
            458 Walkman Dr.
            Suite #292
        city    : Royal Oak
        state   : MI
        postal  : 48046
ship-to: *id001
product:
    - sku         : BL394D
      quantity    : 4
      description : Basketball
      price       : 450.00
    - sku         : BL4438H
      quantity    : 1
      description : Super Hoop
      price       : 2392.00
tax  : 251.42
total: 4443.52
comments: >
    Late afternoon is best.
    Backup contact is Nancy
    Billsmer @ 338-4338.
		"""
		Then I expect HTTP code <code>
		And I expect content contains
"""
bill-to: &id001
    address:
        city: Royal Oak
        lines: '458 Walkman Dr.

            Suite #292

            '
        postal: 48046
        state: MI
    family: Dumars
    given: Chris
comments: Late afternoon is best. Backup contact is Nancy Billsmer @ 338-4338.
date: 2001-01-23
invoice: 34843
product:
-   description: Basketball
    price: 450.0
    quantity: 4
    sku: BL394D
-   description: Super Hoop
    price: 2392.0
    quantity: 1
    sku: BL4438H
ship-to: *id001
tax: 251.42
total: 4443.52
"""
		
		Examples:
			| method	| code	|
			| POST		| 201	|
			| PUT		| 200	|			
			
	@yaml
	Scenario Outline: Handle invalid YAML data
		When as user 'None:None' I <method> 'http://127.0.0.1:8080/post/yaml' with YAML
		"""
- test
{test}
		"""
		Then I expect HTTP code 400
		And I expect content contains 'Unable to parse YAML body: while scanning a simple key'
		
		Examples:
			| method	| 
			| POST		| 
			| PUT		| 		
			
	@json @yaml @xml @route_content_type
	Scenario Outline: Route by incoming content type
		When I prepare HTTP header 'content-type' = '<content>'
		When as user 'None:None' I <method> 'http://127.0.0.1:8080/post/by/content' with <type> body '<body>'
		Then I expect HTTP code <code>
		And I expect content contains '<content>'
		
		Examples:
			| method	| type		| body				| content				| code	| 
			| POST		| JSON		| {"test":2}		| application/json	 	| 201	|
			| POST		| XML		| <test>1</test>	| application/xml	 	| 201	|
			| POST		| XML		| <test>1</test>	| text/xml			 	| 201	|
			| POST		| YAML		| test: 2			| text/yaml			 	| 201	|
			| PUT		| JSON		| {"test":2}		| application/json	 	| 200	|
			| PUT		| XML		| <test>1</test>	| text/xml			 	| 200	|
			| PUT		| XML		| <test>1</test>	| application/xml	 	| 200	|
			| PUT		| YAML		| test: 2			| text/yaml			 	| 200	|
			