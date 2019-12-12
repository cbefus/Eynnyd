.. _tutorial_response_interceptors:

Tutorial: Response Interceptors
===============================

This tutorial builds on what we saw in our :ref:`request interceptor tutorial <tutorial_request_interceptors>` so
you probably want to read that if you haven't yet.  All we are going to do is add a
:ref:`response interceptor <interceptors>` which logs every response leaving the application.   First we
will show you the code and then we will explain the *relevant* parts (AKA the parts not in the prior tutorials).

.. code:: python

    # hello_world_app.py
    import logging

    from eynnyd import RoutesBuilder
    from eynnyd import EynnydWebappBuilder
    from eynnyd import ResponseBuilder
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

    def build_application():
        routes = \
            RoutesBuilder() \
                .add_request_interceptor("/hello", log_request) \
                .add_handler("GET", "/hello", hello_world) \
                .add_response_interceptor("/hello", log_response)\
                .build()

        return EynnydWebappBuilder() \
                .set_routes(routes) \
                .build()

    application = build_application()

Only minor changes are made from the request interceptor tutorial, in particular the response interceptor method
and the routing connection of the response interceptor.

The Response Interceptor Code
-----------------------------
Our response interceptor is called :code:`log_response` and it looks like:

.. code:: python

    def log_response(request, response):
        LOG.info("Built Response: {s} for Request: {r}".format(s=response, r=request))
        return response

Response interceptors are passed both the request (modified by any request interceptors it has passed through) and
the response (either from the handler which created it or any prior response interceptors who may have changed
it). It returns a response and this case we are simply returning the response we were passed.

The response returned is the response that will be passed to any follow up response interceptors or, if this is the
final one, sent to the client. You can use this to either modify the response you are given (Ideally through building
a clone) or return a completely different response.


Routing Responses Through The Response Interceptor
------------------------------------------------

The other relevant change to prior tutorials is the adding of the response interceptors route to
:code:`RoutesBuilder`.

.. code:: python

    routes = \
        RoutesBuilder() \
            .add_request_interceptor("/hello", log_request) \
            .add_handler("GET", "/hello", hello_world) \
            .add_response_interceptor("/hello", log_response) \
            .build()

Here we have set it up so that any response from a route down the :code:`/hello` path would be logged.  This includes
routes like :code:`/hello/more/path/parts`.

The response interceptors run after a handler has created a response from the request. You can have as many
response interceptors as you please, even at the same level. This allows you to have small, single purpose,
interceptors that are easy to test and maintain.

Response interceptors run in priority of inside out (more specific first to less specific) and first in first
out (the order they are registered with the builder).


