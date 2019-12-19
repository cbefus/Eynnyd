.. _tutorial_hello_world:

Tutorial: Hello World
=====================

This is our most basic of tutorials.  How can we create an endpoint which when hit with a blank **GET** request it
returns the text "Hello World".  First we will show you the code and then we will explain the parts.

.. code:: python

    # hello_world_app.py
    from eynnyd import RoutesBuilder
    from eynnyd import EynnydWebappBuilder
    from eynnyd import ResponseBuilder
    from http import HTTPStatus

    def hello_world(request):
        return ResponseBuilder()\
            .set_status(HTTPStatus.OK)\
            .set_utf8_body("Hello World")\
            .build()

    def build_application():
        routes = \
            RoutesBuilder()\
                .add_handler("GET", "/hello", hello_world)\
                .build()

        return EynnydWebappBuilder()\
                .set_routes(routes)\
                .build()

    application = build_application()

Simple right?  Lets look at the various parts.

Simple Request Handler
----------------------
Our request :term:`Handler` is called **hello_world**. It looks like:

.. code:: python

    def hello_world(request):
        return ResponseBuilder()\
            .set_status(HTTPStatus.OK)\
            .set_utf8_body("Hello World")\
            .build()

It's simply a function which takes a :ref:`request <request>` and returns a :ref:`response <response>`.  Many
other frameworks provide you with both a request and response as inputs to your :term:`Handler`\s.  This is exploiting
output parameters and is generally a violation of Clean Code.  We prefer to use returns for outputs and reserve
parameters for inputs.  For the purposes of this :term:`Handler`, we don't care anything about the request, all we want
to do is return a response with the content "Hello World".

We are using Eynnyds built in :ref:`ResponseBuilder <response>`.
to construct a response.  It is possible to build responses yourself, but the :code:`ResponseBuilder` is a convenient
tool for doing it succinctly.

For our response we are returning a status of :code:`OK`, which evaluates to a code of :code:`200`.  We could
have left this :code:`set_status(HTTPStatus.OK)` line out though, because Eynnyd uses :code:`OK` as the default
response status. We added it here to give you a clear example of how to set the status.

For our body we are using the :code:`set_utf8_body("Hello World")` method.  You can set several different kinds
of bodies on your response using the :code:`ResponseBuilder` depending on what content you want to send (for
example: Steaming, Byte, Iterable, etc.).

Finally we call the :code:`build()` method on the :code:`ResponseBuilder`.  This method tells the
:code:`ResponseBuilder` to create the response.  You might note that we use the
`Builder Pattern <https://en.wikipedia.org/wiki/Builder_pattern>`__ a lot in Eynnyd.  For things that have
default values, require validation on inputs, and can be built up over time, we believe the Builder pattern to
be a valid way of separating the concerns of building something, from using something.  This ties into the
Clean Code Philosophy that objects should do one thing.


Building Routes
---------------
Organizing and wiring up your :term:`Route`\s to the code they execute is a single responsibility.  This is why we don't
like then :term:`Route`\s are defined at the definition site (in some frameworks) or as part of the building of the
webapp itself (in other frameworks).  In our code above, building the :term:`Route`\s looks like:

.. code:: python

        routes = \
            RoutesBuilder()\
                .add_handler("GET", "/hello", hello_world)\
                .build()

The key here is that we have added a :term:`Handler` for any request using the HTTP method :code:`GET` on
path :code:`/hello` will execute the :term:`Handler` code inside our :code:`hello_world` method.

After this we call the :code:`build()` method and our :code:`routes` variable now is assigned to a built
routing system.


Building the Webapp
-------------------
Next we have to build the actual Web Application itself.  We do this with code that looks like:

.. code:: python

        return EynnydWebappBuilder()\
                .set_routes(routes)\
                .build()

Here we use the :code:`set_routes` method to pass our built :term:`Route`\s from above to the webapp so that it can
direct requests to the right place.

After this we call the :code:`build()` method and return a fully ready to use Web Application.


Setting the Application Variable
--------------------------------

The last line of our code assigns the global variable named :code:`application` to the result of our
:code:`build_application()` method (which is a built :code:`EynnydWebapp`). This is a WSGI standard
allowing the server to connect into your application.
