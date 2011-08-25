'''
Created on 2011-08-25

@author: jacekf
'''

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="CorePost",
    version="0.0.1",
    author="Jacek Furmankiewicz",
    author_email="jacek99@gmail.com",
    description=("A Twisted Web REST micro-framework"),
    license="BSD",
    keywords="twisted rest flask sinatra get post put delete web",
    url="https://github.com/jacek99/corepost",
    packages=['corepost', ],
    long_description=read('README.md'),
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
         'twisted.internet.processes>=1.0b1'
    ],
      
)
