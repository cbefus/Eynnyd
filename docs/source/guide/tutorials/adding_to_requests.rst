.. _tutorial_adding_to_requests:

Tutorial: Adding Values To Requests
===================================

:ref:`Requests <request>` are preloaded in Eynnyd with all the values from the raw WSGI request. However, as you
are processing your request, you may wish to add additional details to it.  For example, on routes secured by a
session, you may want to load that session from your database in an
:ref:`request interceptor <tutorial_request_interceptors>` and put that loaded value onto your request for later
use (without reloading it).  Because python allows you to manipulate objects after they have been built, you
could do this simply by doing :code:`request.session = session_dao.get_session(request.headers["session"])` but
that wouldn't be very explicit and mutation like this can lead to hidden bugs, surprised readers, and much more.
A more explicit way of doing this is shown below.

Some might argue that the mutation method we just talked about is more "pythonic" than the explicit version we
are about to show you, however we would direct them to the zen of python (type :code:`import this` into any
python terminal) which specifically (and correctly) states: "Explicit is better than implicit".

As a simple example, let's assume we want to add a random ID to every request so that when we log things about it
the ID can be matched up.

This tutorial builds on the :ref:`response interceptors tutorial <tutorial_response_interceptors>` so if you have
not read that yet, and you find something confusing in here, it is recommended you look there for your answer.
First we will show you the code and then we will explain the *relevant* parts (AKA the parts not in the prior
tutorials).

.. code:: python

    # hello_world_app.py
    import logging

    from eynnyd import AbstractRequest
    from eynnyd import RoutesBuilder
    from eynnyd import EynnydWebappBuilder
    from eynnyd import ResponseBuilder
    from eynnyd import ErrorHandlersBuilder

    from http import HTTPStatus
    import uuid

    LOG = logging.getLogger("hello_world_app")

    class IDEnhancedRequest(AbstractRequest):

        def __init__(self, original_request, request_id):
            self._request_id = request_id
            self._original_request = original_request

        @property
        def request_id(self):
            return self._request_id

        @property
        def http_method(self):
            return self._original_request.http_method

        @property
        def request_uri(self):
            return self._original_request.request_uri

        @property
        def forwarded_request_uri(self):
            return self._original_request.forwarded_request_uri

        @property
        def headers(self):
            return self._original_request.headers

        @property
        def client_ip_address(self):
            return self._original_request.client_ip_address

        @property
        def cookies(self):
            return self._original_request.cookies

        @property
        def query_parameters(self):
            return self._original_request.query_parameters

        @property
        def path_parameters(self):
            return self._original_request.path_parameters

        @property
        def byte_body(self):
            return self._original_request.byte_body

        @property
        def utf8_body(self):
            return self._original_request.utf8_body

        def __str__(self):
            return "[{i}]<{m} {p}>".format(i=self._request_id, m=self.http_method, p=self.request_uri)

    def hello_world(request):
        return ResponseBuilder() \
            .set_status(HTTPStatus.OK) \
            .set_utf8_body("Hello World")\
            .build()

    def add_id_to_request(request):
        return IDEnhancedRequest(request, uuid.uuid4())

    def log_request(request):
        LOG.info("Got Request: {r}".format(r=request))
        return request

    def log_response(request, response):
        LOG.info("Built Response: {s} for Request: {r}".format(s=response, r=request))
        return response

    def build_application():
        routes = \
            RoutesBuilder() \
                .add_request_interceptor("/", add_id_to_request) \
                .add_request_interceptor("/", log_request) \
                .add_handler("GET", "/hello", hello_world) \
                .add_response_interceptor("/", log_response)\
                .build()

        return EynnydWebappBuilder() \
                .set_routes(routes) \
                .build()

    application = build_application()

New Imports
-----------
For our new work we need two new imports.

.. code:: python

    from eynnyd import AbstractRequest
    ...
    import uuid

The AbstractRequest represents all the functionality a request must contain (at minimum). These values are already
provided to your code, loaded from the WSGI server.  We are also using the uuid module here to generate us
random IDs.  Collisions this way are pretty uncommon and since these IDs are short lived (only for the duration of a
request) we feel this method is pretty reasonable.

Building An Explicit Request Wrapper Class
------------------------------------------
We now build a class which implements our Eynnyd :code:`AbstractRequest` from above explicitly and it also provides
us with a :code:`request_id property`.

.. code:: python

    class IDEnhancedRequest(AbstractRequest):

        def __init__(self, original_request, request_id):
            self._request_id = request_id
            self._original_request = original_request

        @property
        def request_id(self):
            return self._request_id

        @property
        def http_method(self):
            return self._original_request.http_method

        @property
        def request_uri(self):
            return self._original_request.request_uri

        @property
        def forwarded_request_uri(self):
            return self._original_request.forwarded_request_uri

        @property
        def headers(self):
            return self._original_request.headers

        @property
        def client_ip_address(self):
            return self._original_request.client_ip_address

        @property
        def cookies(self):
            return self._original_request.cookies

        @property
        def query_parameters(self):
            return self._original_request.query_parameters

        @property
        def path_parameters(self):
            return self._original_request.path_parameters

        @property
        def byte_body(self):
            return self._original_request.byte_body

        @property
        def utf8_body(self):
            return self._original_request.utf8_body

        def __str__(self):
            return "[{i}]<{m} {p}>".format(i=self._request_id, m=self.http_method, p=self.request_uri)

There are 3 unique things to note about this class.  The first is that every property except the :code:`request_id`
property just returns the value from the original request object.  The second note-worthy item is the
:code:`request_id` property itself, which just returns any id set in the constructor. And finally, it is also
worth noting we have updated our :code:`__str__` method, which means that any logging of this request will now
start with a prefixed request id value.


Updating the Request
--------------------
Now we just need a :ref:`request interceptor <tutorial_request_interceptors>` to update our incoming request
with new values.

.. code:: python

    def add_id_to_request(request):
        return IDEnhancedRequest(request, uuid.uuid4())

Because :code:`IDEnhancedRequest` extends :code:`AbstractRequest` this code is legal (wont fail Eynnyd's request
interceptor validation).  All we are doing is returning the wrapped request with a newly added, random id.

Adding the Interceptor
----------------------
Finally, we just need to add this interceptor to our routes at the root level and make sure it runs before all
other interceptors.

.. code:: python

    def build_application():
        routes = \
            RoutesBuilder() \
                .add_request_interceptor("/", add_id_to_request) \
                .add_request_interceptor("/", log_request) \
                .add_handler("GET", "/hello", hello_world) \
                .add_response_interceptor("/", log_response)\
                .build()

Note we added this interceptor before the other root interceptors to insure it runs first.  With this change both
the :code:`log_request` request interceptor and the :code:`log_response` response interceptor will log out the
request including our new id value.


