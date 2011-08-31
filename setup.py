"""
Twisted REST micro-framework
================================

Based on *Flask* API, with integrated multiprocessing support for full usage of all CPUs. 
Provides a more Flask/Sinatra-style API on top of the core *twisted.web* APIs.

The simplest possible twisted.web CorePost REST application:

::

    from corepost.web import CorePost
    from corepost.enums import Http
    
    app = CorePost()
    
    @app.route("/",Http.GET)
    def root(request,**kwargs):
        return request.path
    
    @app.route("/test",Http.GET)
    def test(request,**kwargs):
        return request.path
    
    @app.route("/test/<int:numericid>",Http.GET)
    def test_get_resources(request,numericid,**kwargs):
        return "%s" % numericid
    
    if __name__ == '__main__':
        app.run()

Links
`````

* `website <http://github.com/jacek99/corepost>`_
* `Twisted <http://twistedmatrix.com>`_

"""

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return  open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="CorePost",
    version="0.0.4",
    author="Jacek Furmankiewicz",
    author_email="jacek99@gmail.com",
    description=("A Twisted Web REST micro-framework"),
    license="BSD",
    keywords="twisted rest flask sinatra get post put delete web",
    url="https://github.com/jacek99/corepost",
    packages=['corepost', ],
    long_description=__doc__,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
         'twisted>=11.0.0',
         'httplib2>=0.7.1',
         'freshen>=0.2',
         'formencode>=1.2.4',
    ],
      
)
