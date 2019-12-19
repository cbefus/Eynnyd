.. _tutorial_error_handlers:

Tutorial: Error Handlers
========================

Error handlers are code that should execute if an exception is raised somewhere in the web application.  Eynnyd
provides you with a way to associate an Exception type with a function to execute if that exception is raised.

An error handling function takes two forms: pre_response and post_response.  More on this below.

This tutorial builds on the prior one on :ref:`response interceptors <tutorial_response_interceptors>, so if
there is a piece you don't understand here it was likely covered there.

First we will show you the code and then we will explain the *relevant* parts (AKA the parts not in the prior
tutorials).

.. code:: python

    # hello_world_app.py
    import logging

    from eynnyd import RoutesBuilder
    from eynnyd import EynnydWebappBuilder
    from eynnyd import ResponseBuilder
    from eynnyd import ErrorHandlersBuilder
    from http import HTTPStatus

    LOG = logging.getLogger("hello_world_app")

    def hello_world(request):
        return ResponseBuilder() \
            .set_status(HTTPStatus.OK) \
            .set_utf8_body("Hello World")\
            .build()

    def log_request(request):
        LOG.info("Got Request: {r}".format(r=request))
        return request

    def log_response(request, response):
        LOG.info("Built Response: {s} for Request: {r}".format(s=response, r=request))
        return response

    class UnAuthorizedAccessAttemptException(Exception):
        pass

    def raise_unauth_for_missing_header(request):
        if "auth" not in request.headers:
            raise UnAuthorizedAccessAttemptException("Must have an auth header to be granted access.")
        return request

    def handle_unauthorized_error(error_thrown, request):
        LOG.warn("Unauthorized attempt on url: {u}".format(u=request.request_uri))
        return RoutesBuilder() \
            .set_status(HTTPStatus.UNAUTHORIZED) \
            .set_utf8_body("Authorization failed with error: {e}".format(e=str(error_thrown))) \
            .build()

    def build_application():
        routes = \
            RoutesBuilder() \
                .add_request_interceptor("/", raise_unauth_for_missing_header) \
                .add_request_interceptor("/hello", log_request) \
                .add_handler("GET", "/hello", hello_world) \
                .add_response_interceptor("/hello", log_response)\
                .build()

        error_handlers = \
            ErrorHandlersBuilder() \
                .add_pre_response_error_handler(UnAuthorizedAccessAttemptException, handle_unauthorized_error) \
                .build()

        return EynnydWebappBuilder() \
                .set_routes(routes) \
                .set_error_handlers(error_handlers) \
                .build()

    application = build_application()

It should be noted that, so far in our tutorials, we have been using stand alone functions for all of our code.
There functions can of course be encapsulated into objects so that a function like
:code:`def log_request(request)` could instead be :code:`def log_request(self, request)` on a class and we
would then use it at our callsites as :code:`logging_interceptors.log_request`.

Building a Python Named Exception
---------------------------------
The first relevant new piece to this tutorial is a custom named exception.  Named Exceptions are superior to
built in exceptions for a variety of reasons, mainly readability and allowing for explicit handling.  That
being said, you can use the built in python exceptions for this same purpose.

We haven't done anything special with this named exception so it should look like your typical usage of python:

.. code:: python

    class UnAuthorizedAccessAttemptException(Exception):
        pass

Here we have defined an exception to be used when access is attempted which should be denied as unauthorized.


Raising an Exception
--------------------

Now that we have an exception we need somewhere to raise it.  For this tutorial we are going to do that in
a new request :ref:`Interceptor`.

.. code:: python

    def raise_unauth_for_missing_header(request):
        if "auth" not in request.headers:
            raise UnAuthorizedAccessAttemptException("Must have an auth header to be granted access.")
        return request

Our new request :ref:`Interceptor` checks if there is a header keyed on "auth". If not it raises our named exception.
Of course we probably want to do more validation on this header to confirm that even if it is present it is
valid, but we can leave that to other :ref:`Interceptor`s (and out of this tutorial for simplicity).

The other thing we need to do, as expected is to register this request :ref:`Interceptor` into our :ref:`Route`s:

.. code:: python

    routes = \
        RoutesBuilder() \
            .add_request_interceptor("/", raise_unauth_for_missing_header) \
            .add_request_interceptor("/hello", log_request) \
            .add_handler("GET", "/hello", hello_world) \
            .add_response_interceptor("/hello", log_response)\
            .build()

As you can see, this :ref:`Interceptor` should run for all requests by using the root path "/".

Writing a Error Handling Method
-------------------------------

Next we need code that we want to run if this error is thrown.  That looks like:

.. code:: python

    def handle_unauthorized_error(error_thrown, request):
        LOG.warn("Unauthorized attempt on url: {u}".format(u=request.request_uri))
        return RoutesBuilder() \
            .set_status(HTTPStatus.UNAUTHORIZED) \
            .set_utf8_body("Authorization failed with error: {e}".format(e=str(error_thrown))) \
            .build()

This function is built to handle errors thrown prior to having a response object (which is why it only takes
parameters for the :code:`error_thrown` and the :code:`request`.  If we threw our error from a :term:`Handler` this
code would look exactly the same. However, if we threw an error from a response :ref:`Interceptor` then this code
would be different (the function would take a third parameter for the response).

:ref:`Error Handler`s return responses. In this case the response we are going to return is an :code:`UNAUTHORIZED`
status with a body of text describing the errors message.

Associating an Error Type with An Error Handler
-----------------------------------------------

Next we need to associate our named exception with the code we just wrote to handle that exception being
thrown.  We do this using the Eynnyd :code:`ErrorHandlersBuilder` class:

.. code:: python

    error_handlers = \
        ErrorHandlersBuilder() \
            .add_pre_response_error_handler(UnAuthorizedAccessAttemptException, handle_unauthorized_error) \
            .build()

You can see we are associating our new handler :code:`handle_unauthorized_error` to the named exception
:code:`UnAuthorizedAccessAttemptException` by calling :code:`add_pre_response_error_handler`.  It should be
obvious that this method only works for errors raised from a pre response location (request :ref:`Interceptor`s and
handlers).  Once there is a response (in response :ref:`Interceptor`s) you would want to associate your exception
with the code to call using a similar method called: :code:`add_post_response_error_handler`.

Adding Error Handlers To The Web App
------------------------------------

Finally we can add our :ref:`Error Handler`s to the Eynnyd webapp using the :code:`EynnydWebappBuilder`:

.. code:: python

    return EynnydWebappBuilder() \
            .set_routes(routes) \
            .set_error_handlers(error_handlers) \
            .build()

Very similar to setting our routing object from earlier tutorials.