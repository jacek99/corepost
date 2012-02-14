Using step definitions from: '../steps'

@issues
Feature: Issues
	Fixes for issues reported on github
	
	@issue1
	Scenario: Issue 1 (unable to access self.var in a router method)
		Given 'home_resource' is running
		When as user 'None:None' I GET 'http://127.0.0.1:8080/issues/1'
		Then I expect HTTP code 200
		And I expect content contains 'issue 1'

