'''
Common Freshen BDD steps

@author: jacekf
'''
import httplib2
from freshen import * #@UnusedWildImport

##################################
# BEFORE / AFTER
##################################

@Before
def setup():
    scc.processes = []

@After
def cleanup():
    # shut down processes
    for process in scc.processes:
        process.terminate()

##################################
# GIVEN
##################################

@Given("'(.+)' is running")
def given_process_is_running(processname):
    pass

##################################
# WHEN
##################################

@When("^as user '(.+):(.+)' I (GET|DELETE) '(.+)'\s*$")
def when_as_user_i_send_get_delete_to_url(user,passord,method,url):
    pass

@When("^as user '(.+):(.+)' I (POST|PUT) '(.+)' with '(.+)'\s*$")
def when_as_user_i_send_post_put_to_url(user,password,method,url,params):
    pass

@When("^as user '(.+):(.+)' I (POST|PUT) '(.+)' (XML|JSON)\s*$")
def when_as_user_i_send_post_put_xml_json_to_url(payload,user,passord,method,url):
    pass

##################################
# THEN
##################################

@Then("^I expect HTTP code \d+\s*$")
def expect_http_code(code):
    pass

@Then("^I expect content contains\s*$")
def expect_content(conntent):
    pass

@Then("^I expect header '(.+)' contains '(.+)'\s*$")
def expect_header_contains(conntent):
    pass


