'''
Common Freshen BDD steps

@author: jacekf
'''
from multiprocessing import Process
import httplib2, json, re, time, string
from freshen import Before, Given, When, Then, scc, glc, assert_equals, assert_true #@UnresolvedImport
from urllib import urlencode
from corepost.test.home_resource import run_app_home
from corepost.test.multi_resource import run_app_multi
from corepost.test.arguments import run_app_arguments

apps = {'home_resource' : run_app_home,'multi_resource':run_app_multi,'arguments':run_app_arguments}

NULL = 'None'

def as_dict(parameters):
    dict_val = {}
    for pair in parameters.split('&') : 
        params = pair.split('=', 1)
        if (params[0] != None) and (len(params) == 2):
            dict_val[params[0]] = params[1]
    return dict_val

##################################
# BEFORE / AFTER
##################################

@Before
def setup(slc):
    scc.http_headers = {}

##################################
# GIVEN
##################################

@Given(r"^'(.+)' is running\s*$")
def given_process_is_running(processname):
    if glc.processes == None:
        glc.processes = {}

    if processname not in glc.processes:
        # start a process only once, keep it running
        # to make test runs faster
        process = Process(target=apps[processname])
        process.daemon = True
        process.start()
        time.sleep(0.25) # let it start up
        glc.processes[processname] = process

##################################
# WHEN
##################################

@When(r"^as user '(.+):(.+)' I (GET|DELETE) '(.+)'\s*$")
def when_as_user_i_send_get_delete_to_url(user,password,method,url):
    h = httplib2.Http()
    h.follow_redirects = False
    h.add_credentials(user, password)
    scc.response, scc.content = h.request(url, method, headers = scc.http_headers)

@When(r"^as user '(.+):(.+)' I (POST|PUT) '(.+)' with '(.+)'\s*$")
def when_as_user_i_send_post_put_to_url(user,password,method,url,params):
    h = httplib2.Http()
    h.follow_redirects = False
    h.add_credentials(user, password)
    scc.http_headers['Content-type'] = 'application/x-www-form-urlencoded'
    scc.response, scc.content = h.request(url, method, urlencode(as_dict(params)), headers = scc.http_headers)

@When(r"^as user '(.+):(.+)' I (POST|PUT) '(.+)' with (XML|JSON|YAML) body '(.+)'\s*$")
def when_as_user_i_send_post_put_xml_json_to_url(user,password,method,url,request_type,body):
    when_as_user_i_send_post_put_xml_json_to_url_multiline(body,user,password,method,url,request_type)

@When(r"^as user '(.+):(.+)' I (POST|PUT) '(.+)' with (XML|JSON|YAML)\s*$")
def when_as_user_i_send_post_put_xml_json_to_url_multiline(body,user,password,method,url,request_type):
    h = httplib2.Http()
    h.follow_redirects = False
    h.add_credentials(user, password)
    if request_type == "JSON":
        scc.http_headers['Content-type'] = 'application/json'
    elif request_type == "XML":
        scc.http_headers['Content-type'] = 'text/xml'
    elif request_type == "YAML":
        scc.http_headers['Content-type'] = 'text/yaml'        
    scc.response, scc.content = h.request(url, method, body, headers = scc.http_headers)

@When("I prepare HTTP header '(.*)' = '(.*)'")
def when_i_define_http_header_with_value(header,value):
    if header != NULL:
        scc.http_headers[header] = value

##################################
# THEN
##################################
def transform_content(content):
    """Support embedded newlines"""
    if content != None:
        return string.replace(content,"\\n","\n")
    else:
        return None

@Then(r"^I expect HTTP code (\d+)\s*$")
def expect_http_code(code):
    assert_equals(int(code),int(scc.response.status), msg="%s != %s\n%s\n%s" % (code,scc.response.status,scc.response,scc.content))

@Then(r"^I expect content contains '(.+)'\s*$")
def expect_content(content):
    content = transform_content(content)
    assert_true(scc.content.find(content) >= 0,"Did not find:\n%s\nin content:\n%s" % (content,scc.content)) 

@Then(r"^I expect content contains\s*$")
def expect_content_multiline(content):
    content = transform_content(content)
    assert_true(scc.content.find(content) >= 0,"Did not find:\n%s\nin content:\n%s" % (content,scc.content)) 

@Then(r"^I expect '([^']*)' header matches '([^']*)'\s*$")
def then_check_http_header_matches(header,regex):
    assert_true(re.search(regex,scc.response[header.lower()], re.X | re.I) != None, 
                "the regex %s does not match the response\n%s" % (regex, scc.response[header.lower()])) 

@Then("^I expect JSON content\s*$")
def then_i_expect_json(content):
    expected_json = json.loads(content) 
    expected_json_sorted = json.dumps(expected_json,sort_keys=True,indent=4)
    received_json = json.loads(scc.content)
    received_json_sorted = json.dumps(received_json,sort_keys=True,indent=4)
    assert_equals(expected_json_sorted,received_json_sorted,"Expected JSON\n%s\n*** actual ****\n%s" % (expected_json_sorted,received_json_sorted))

