Introduction
============

What is CorePost?
-----------------

CorePost is a Python REST micro-framework. It is meant for building enterprise-grade REST server applications that provide
API services to other applications and/or a UI layer (coded in any framework or language).

More importantly, CorePost is an asynchronous I/O web framework (similar to Node.js).
Hence it relies on asynchronous I/O operations, which are extremely efficient, but somewhat more complicated to code.

Fortunately, CorePost does not create it's own async I/O library, but instead uses under the mature, well documented
and extremely well designed Twisted library, in particular its web layer (known simply as twisted.web)

Coupled with a JIT runtime like PyPy, this should give you the ability to develop REST server side applications
that will be extremely performant in production, yet (hopefully) fun and productive to develop.

What is Twisted?  
----------------

Twisted is a very mature Python async I/O network toolkit:

http://twistedmatrix.com/trac/

Understanding core principles behind Twisted and its APIs is required (at least at a basic level) before coding any CorePost application.

Hence we recommend either reading the very thorough developer's guide:

http://twistedmatrix.com/documents/current/core/howto/book.pdf

or the excellent Twisted tutorials from Dave Peticolas:

http://krondo.com/blog/?page_id=1327

In particular, understanding the core Twisted Deferred object (and its productive inline callback approach) are crucial
to productive usage of Twisted APIs for writing asynchronous web applications.

What does CorePost add on top of Twisted Web?
---------------------------------------------

Mostly productivity features that take of low-level plumbing such as:

* routing request to handler methods
* automatic parsing of JSON/YAML/XML input
* automatic conversion of Python objects and classes to JSON / YAML / XML formats
* simplified exception handling
* custom request / response filters

However, this is a very thin layer. Once you get to write some serious code that interacts with an external system (e.g. a SQL database)
you are writing a hard-code Twisted web application. CorePost is just there to make it easier for you and let you focus on business logic,
while letting it take care of common required plumbing. That's it.

A CorePost application is nothing more than a *twisted.web* application under the hood.

Why would I use CorePost instead of Node.js?
--------------------------------------------

As you develop more Twisted code, you will realize how its elegant and powerful *Deferred* object
(and especially inline callbacks) make developing *readable* asynchronous code much more pleasant than any other solution.