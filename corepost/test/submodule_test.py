'''
A CorePost submodule that can be merged into the main CorePost Resource
'''

from corepost.web import CorePost
from corepost.enums import Http

submodule = CorePost()
submodule.isLeaf = True

@submodule.route("/test",Http.GET)
def submodule_get(request,**kwargs):
    return request.path