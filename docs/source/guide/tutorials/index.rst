Tutorials
=========

We will build up our collection of Tutorials over time to include as many real world situations as possible.
Our tutorials use Eynnyd the way we prefer **but this is not the only way to use the framework.**

For example, we like to using `Fluent Interfaces <https://en.wikipedia.org/wiki/Fluent_interface>`__ and our
framework allows for that, but it also allows for you to not work this way.

A Fluent usage might look like:

.. code:: python

    routes = \
        RoutesBuilder() \
            .add_request_interceptor("/hello", log_request) \
            .add_handler("GET", "/hello", hello_world) \
            .add_response_interceptor("/hello", log_response) \
            .build()

but this would work just as well if you wrote it as:

.. code:: python

    routes_builder = RoutesBuilder()
    routes_builder.add_request_interceptor("/hello", log_request)
    routes_builder.add_handler("GET", "/hello", hello_world)
    routes_builder.add_response_interceptor("/hello", log_response)
    routes = routes_builder.build()

Use the framework the way you prefer, who are we to judge?

.. toctree::
   :maxdepth: 2

   hello_world
   request_interceptors
   response_interceptors
   error_handlers
   decorators
