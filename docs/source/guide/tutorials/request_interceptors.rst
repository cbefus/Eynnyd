.. _tutorial_request_interceptors:

Tutorial: Request Interceptors
==============================

This tutorial builds on what we saw in our :ref:`hello world tutorial <tutorial_hello_world>` so you probably want to
read that if you haven't yet.  All we are going to do is add a :code:`request interceptor` which
logs every request coming into the application.   First we will show you the code and then we will explain the
*relevant* parts (AKA the parts not in the hello world tutorial).

.. code:: python

    # hello_world_app.py
    import logging

    from eynnyd import RoutesBuilder
    from eynnyd import EynnydWebappBuilder
    from eynnyd import ResponseBuilder
    from http import HTTPStatus

    LOG = logging.getLogger("hello_world_app")

    def hello_world(request):
        return ResponseBuilder()\
            .set_status(HTTPStatus.OK)\
            .set_utf8_body("Hello World")\
            .build()

    def log_request(request):
        LOG.info("Got Request: {r}".format(r=request))
        return request

    def build_application():
        routes = \
            RoutesBuilder()\
                .add_request_interceptor("/hello", log_request)\
                .add_handler("GET", "/hello", hello_world)\
                .build()

        return EynnydWebappBuilder()\
                .set_routes(routes)\
                .build()

    application = build_application()

Only minor changes to the hello world tutorial are added here.

The Request Interceptor Code
----------------------------

Our request :term:`Interceptor` is called :code:`log_request` and it looks like:

.. code:: python

    def log_request(request):
        LOG.info("Got Request: {r}".format(r=request))
        return request

As you can see our :term:`Interceptor` is a function which takes a request and returns a request.  In this case we
are returning the same request we were given.  All we are doing here is logging the string representation
of the request to an info level log line.  However, if we had mutated the request here (or better yet, created
a new request with slightly updated values), **the request we return is the request which will be passed on
from this point** through the code**. For example, perhaps you would like to attach a new header to your request,
you could do that here and all following code would be given that new request object.


Routing Requests Through The Request Interceptor
------------------------------------------------

The other relevant piece of code here is the registering of the :term:`Interceptor` to specific :term:`Route`\s. It looks like:

.. code:: python

    routes = \
        RoutesBuilder()\
            .add_request_interceptor("/hello", log_request)\
            .add_handler("GET", "/hello", hello_world)\
            .build()

As you can see, we are adding a request :term:`Interceptor` which should run for any request on the path :code:`/hello`.
This includes :term:`Route`\s like :code:`/hello/more/path/parts`.

The request :term:`Interceptor`\s will run before a matching :term:`Handler` is run. You can register many request :term:`Interceptor`\s,
even at the same path level.  This allows you to have small, single purpose :term:`Interceptor`\s, that are easy to test
and maintain. Other frameworks only allow you to have a single :term:`Interceptor` for all requests which leads to messy
implementations.

Request :term:`Interceptor`\s run in priority of outside in (so :term:`Interceptor`\s at the base path will run before :term:`Interceptor`\s
at a more specific path) and then first in first out (the order added to the RoutesBuilder).