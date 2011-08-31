'''
Argument extraction tests
@author: jacekf
'''

from corepost.web import CorePost
from corepost.enums import Http

app = CorePost()

@app.route("/int/<int:intarg>/float/<float:floatarg>/string/<stringarg>",Http.GET)
def test(request,intarg,floatarg,stringarg,**kwargs):
    args = (intarg,floatarg,stringarg)
    return "%s" % map(lambda x: (type(x),x),args)

def run_app_arguments():
    app.run(8082)