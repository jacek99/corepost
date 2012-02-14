"""
Twisted REST micro-framework
================================

Based on *Flask* API, with integrated multiprocessing support for full usage of all CPUs. 
Provides a more Flask/Sinatra-style API on top of the core *twisted.web* APIs.
Integrates FormEncode for path, form and query argument validation.

The simplest possible twisted.web CorePost REST application:

::

    from corepost.web import CorePost, route
    from corepost.enums import Http
    
    class RestApp(CorePost):
    
        @route("/",Http.GET)
        def root(self,request,**kwargs):
            return request.path
        
        @route("/test",Http.GET)
        def test(self,request,**kwargs):
            return request.path
        
        @route("/test/<int:numericid>",Http.GET)
        def test_get_resources(self,request,numericid,**kwargs):
            return "%s" % numericid
    
    if __name__ == '__main__':
        app = RestApp()
        app.run()

Links
`````

* `Website <http://github.com/jacek99/corepost>`_
* `Twisted <http://twistedmatrix.com>`_
* `FormEncode <http://www.formencode.org/>`_

Changelog
`````````
* 0.0.9:
     - fix for issue #3 (wrong class passes as 'self' to router method): 
         https://github.com/jacek99/corepost/issues/3 
* 0.0.8:
    - support for serializing of classes to JSON,XML,YAML based on caller's Accept header
    - separate routing functionality from CorePost Resource object, in preparation for future multicore support
* 0.0.7:
    - automatic parsing of incoming content (JSON, YAML, XML)
    - routing by incoming content type
    - automatic response conversion based on caller's Accept header (JSON/YAML
    - support for defer.returnValue() in @inlineCallbacks route methods
* 0.0.6 - redesigned API around classes and methods, rather than functions and global objects (after feedback from Twisted devs)
* 0.0.5 - added FormEncode validation for arguments
* 0.0.4 - path argument extraction, mandatory argument error checking

"""

from setuptools import setup

setup(
    name="CorePost",
    version="0.0.9",
    author="Jacek Furmankiewicz",
    author_email="jacekeadE99@gmail.com",
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
         'formencode>=1.2.4',
         'pyyaml>=3.1.0',
         'jinja2>=2.6',
         'txZMQ>=0.3.1,'
    ],
    tests_require=[
         'httplib2>=0.7.1',
         'freshen>=0.2',
    ],
    zip_safe = True
)
