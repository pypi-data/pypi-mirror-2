Manual
++++++

HTTPKit is a set of services for handling the features of the HTTP protocol
which are useful to simple web applications. It existis in two logical parts:

* Helpers
* Services

The *helpers* are simple functions you can use in any application to
manipulate HTTP data. The *services* use these helpers to provide the ``http``
key for the PipeStack framework and may not be as useful unless you are using
bags.

At the moment the helpers are very simple and provide only the following
functions:

.. autofunction:: httpkit.helper.cookie.set_cookie

.. autofunction:: httpkit.helper.cookie.get_cookie

Let's concentrate on the services. The services are all based on the `PipeStack
Gateway Interface specification <psgi.html>`_ (PSGI). You should read that if
you haven't already.

HTTPService
===========

The API of the HTTPKit services look like this:

Request API:

``bag.environ``
    The underlying environment containing all the HTTP headers as well as
    environment data. Depending on how the application is deployed this could
    be the WSGI environment and contain the WSGI keys too.

Response API:
    
``bag.http_response.status``
    A string representing the HTTP response status. eg ``"200 OK"`` or 
    ``"404 Not Found"``

``bag.http_response.header_list``
    A list of WSGI http header dictionaries. eg 
    ``[dict('Content-Type', 'text/html')]``. 

``bag.http_response.body``
    Either a list of Unicode strings or an iterable which when iterated over
    returns a series of bytes representing the response.

HTTPInputService
================

This service reads the ``wsgi.input`` key from ``bag.environ`` and
parses it to a ``cgi.FieldStorage`` object. If there is no POST data then
``bag.input`` will be ``None``, otherwise you can access the data like
this:

::

    bag.input['name'].getfirst()
    bag.input['name'].getlist()

The ``wsgi.input`` value is replaced with a ``StringIO.StringIO`` object so
that any code dispatched with the WSGI service can parse the data again.

HTTPQueryService
================

This service reads the ``QUERY_STRING`` key from ``bag.environ`` and
parses it to a ``cgi.FieldStorage`` object. If there is no QUERY_STRING then
``bag.query`` will be ``None``, otherwise you can access the data like
this:

::

    bag.query['name'].getfirst()
    bag.query['name'].getlist()


