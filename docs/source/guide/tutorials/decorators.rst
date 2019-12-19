.. _tutorial_decorators:

Tutorial: Decorators
====================

In the previous tutorial on :ref:`tutorial_error_handlers` we saw the use of request :term:`Interceptor`\s to do
simple authorization.  The truth is throwing exceptions like this may be pythonic but it it's a violation
of *using exceptions for control flow*.  Having requests which are not authorized isn't really exceptional
behaviour.

In this Tutorial we will build out an authorization validator using both request :term:`Interceptor`\s and python
decorators.  Some frameworks implement their own versions of decorators (often calling them hooks or muddying
them with their :term:`Interceptor`\s) but this is needless because python decorators are pretty awesome.

Building out a proper authorization cycle also requires talking to a database.  For this tutorial we won't
show the database code as it isn't relevant to the point.

A final change to our prior tutorials is that we will be taking more of an OO approach to our code this time.
We do this for two reasons, first to show you how everything we've done thus far is just as easy in an
OO mindset, and second, because it allows for dependency injection.

With all of that said, first we will show you the full code for this tutorial and then we will work through the
parts piece by piece to explain them further.

.. code:: python

    # auth_example_app.py
    import functools
    import os
    import sys

    from eynnyd import RoutesBuilder
    from eynnyd import EynnydWebappBuilder
    from eynnyd import ResponseBuilder
    from eynnyd import ErrorHandlersBuilder
    from http import HTTPStatus

    from src.config_loader import ConfigLoader
    from src.mysql_db_connection_pool import MySQLDBConnectionPool
    from src.mysql_messages_dao import MySQLMessagesDAO
    from src.mysql_sessions_dao import MySQLSessionsDAO

    class MessagesHandler:

        def __init__(self, messages_dao):
            self._messages_dao = messages_dao

        @request_secured_by_session
        @requires_json_body
        @request_json_field_existence_validation(["user_id"])
        def get_user_messages(request):
            messages = self._messages_dao.get_messages_for_user_id(request.json_body["user_id"])
            return ResponseBuilder() \
                .set_status(HTTPStatus.OK) \
                .set_utf8_body(json.dumps(messages)) \
                .build()


    class RequestSessionBuildingInterceptor:

        def __init__(self, sessions_dao):
            self._sessions_dao = sessions_dao

        def load_session_onto_request(self, request):
            request.session = None
            if "auth" not in request.headers:
                return request

            if not request.headers["auth"]:
                return request

            request.session = self._sessions_dao.get_valid_session_or_none(request.headers["auth"])
            return request


    def request_secured_by_session(decorated_function):
        @functools.wraps(decorated_function)
        def decorator(handler, request, *args, **kwargs):
            if not request.session:
                return ResponseBuilder() \
                    .set_status(HTTPStatus.UNAUTHORIZED) \
                    .set_utf8_body("Request require a valid session. Please login.") \
                    .build()
            return decorated_function
        return decorator


    def build_application():

        configuration = ConfigLoader(os.environ, sys.argv).load()
        database_pool = MySQLDBConnectionPool(configuration.get_database_config())

        messages_dao = MySQLMessagesDAO(database_pool)
        sessions_dao = MySQLSessionsDAO(database_pool)

        request_session_building_interceptor = RequestSessionBuildingInterceptor(sessions_dao)
        messages_handler = MessagesHandler(messages_dao)

        routes = \
            RoutesBuilder() \
                .add_request_interceptor("/", request_session_building_interceptor.load_session_onto_request) \
                .add_handler("GET", "/messages", messages_handler.get_user_messages) \
                .build()

        return EynnydWebappBuilder() \
                .set_routes(routes) \
                .build()

    application = build_application()

So what we have is an application with a single :term:`Route` which returns a list of messages from our database
given a :code:`user_id`.  This :term:`Route` is secured by an authorization header.  We use the request :term:`Interceptor`
:code:`request_session_building_interceptor.load_session_onto_request` to load a valid session onto the
request object and then use the :code:`@request_secured_by_session` decorator to make the decision what to
do if it isn't there.  The value here is that we can now wrap any :term:`Handler` we want to be secured using the
:code:`@request_secured_by_session` but if we have a non secured endpoint (for example a register endpoint)
then we can simply leave off the decorator and it is not secured.  The information about the endpoint being
secured is at the definition site of the function, where it should be.  Because the :term:`Interceptor` is built
ahead of time, database access can be injected into it (where as this would involve something hackish to
do inside the decorator).

Now the :term:`Interceptor` has one job: loading the session onto the request. The decorator has one job: returning
an error response if the valid session does not exist. The :term:`Handler` method has one job: getting the messages
for the user id.

We will discuss all the parts of this code in much further detail below.



The Handler
-----------

First we have our :term:`Handler` who's responsibility is to get messages for a user.  Ideally all other code isn't
in the :term:`Handler` so that we don't obfuscate the code.

.. code:: python

    class MessagesHandler:

        def __init__(self, messages_dao):
            self._messages_dao = messages_dao

        @request_secured_by_session
        @requires_json_body
        @request_json_field_existence_validation(["user_id"])
        def get_user_messages(request):
            messages = self._messages_dao.get_messages_for_user_id(request.json_body["user_id"])
            return ResponseBuilder() \
                .set_status(HTTPStatus.OK) \
                .set_utf8_body(json.dumps(messages)) \
                .build()

Note that the code in the :term:`Handler` function clearly states how we get the messages for the user and nothing
else. However, using decorators we can see that before this function executes we:

1. Secure our request for sessions
2. Validates the body has json content (and in this case loads the json into request.json_body).
3. Validates that the json contains a field keyed on "user_id"

This is a lot of logic that is no longer muddying what our :term:`Handler` does, but is still clearly visible as being
executed for this :term:`Handler`.  More importantly, the many other :term:`Handler` who would need this same functionality
can have it, in a readable fashion, without obfuscating their logic either.

Also different from the other tutorials, this :term:`Handler` is inside an object.  We do this so that we can take
advantage of dependency injection.  We injected a messages data access object (DAO) into this handling class.
This class does not care that this DAO is connecting us to a MySQL database, only that it has a method
called :code:`get_messages_for_user_id` that takes a :code:`user_id` and returns a list of messages.

The Interceptor
---------------

The next piece of code to look at is the class holding our :term:`Interceptor`:

.. code:: python

    class RequestSessionBuildingInterceptor:

        def __init__(self, sessions_dao):
            self._sessions_dao = sessions_dao

        def load_session_onto_request(self, request):
            request.session = None
            if "auth" not in request.headers:
                return request

            if not request.headers["auth"]:
                return request

            request.session = self._sessions_dao.get_valid_session_or_none(request.headers["auth"])
            return request


As in the :term:`Handler` above we have put this method inside a class because we want to exploit dependency
injection of our sessions data access object.

You can quickly see that all this method does is either load a session onto the request from the database
or it sets the value to None.  We actually wouldn't use :code:`None` for this generally, but rather
optionals, but we figured this tutorial was not the platform to discuss that.

As should be expected, this :term:`Interceptor` has nothing to do with getting a response back to the user, it
simply mutates the request, loading new values onto it.  We have removed the unnecessary exception
raising from our :term:`Interceptor` and saved ourselves one less violation of exceptions as control flow.


The Decorator
-------------

Instead of throwing exceptions and using :term:`Error Handler`\s to return a bad response we instead have a
python decorator wrap our :term:`Handler` function.  The code for this decorator looks like:

.. code:: python

    def request_secured_by_session(decorated_function):
        @functools.wraps(decorated_function)
        def decorator(handler, request, *args, **kwargs):
            if not request.session:
                return ResponseBuilder() \
                    .set_status(HTTPStatus.UNAUTHORIZED) \
                    .set_utf8_body("Request require a valid session. Please login.") \
                    .build()
            return decorated_function
        return decorator

All this decorator does is check if the :term:`Interceptor` put a valid session onto the request.  If it didn't we
return an UNAUTHORIZED status response. If a valid session is present we call through to the wrapped function.

Wiring Up Dependencies
----------------------

Another change you might have seen in this tutorial is that we build up a series of objects before we
start building our :term:`Route`\s.  These objects are our dependency chain.  The code looks like:

.. code:: python

    configuration = ConfigLoader(os.environ, sys.argv).load()
    database_pool = MySQLDBConnectionPool(configuration.get_database_config())

    messages_dao = MySQLMessagesDAO(database_pool)
    sessions_dao = MySQLSessionsDAO(database_pool)

    request_session_building_interceptor = RequestSessionBuildingInterceptor(sessions_dao)
    messages_handler = MessagesHandler(messages_dao)

First we have an object which loads configuration from various sources (the environment, command line, and
any configuration files we happen to read in).  We need this configuration to build other dependencies.

Next we have a database pool connection which requires a selection of values from our configuration result.

Then we have two DAOss, the :code:`messages_dao` and the :code:`sessions_dao`.  Note that on the right side
of the assignment here we care that this is a MySQL implementation but on the left we just care that it is
a DAO.  In a statically typed language we would be using an interface on the left, but this is python, so
life is easier.  Note that into the DAOs we inject our database pool. These DAOs dont care about the specifics
of our MySQL driver, only that they can execute sql commands against a database.

Now that we have our DAOs we can build our :term:`Interceptor`\s and :term:`Handler`\s.  For this tutorial we just have the one
of each.  Into each of these we inject our built DAOs.

This kind of dependency build up allows code to be easy to read, debug, extend, and maintain. In fact, in his
book :ref:`Clean Architecture <https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164>`__
Robert C. Martin makes a very strong argument that dependency inversion like this is the only real advantage
OO gave us.  Several other WSGI frameworks prevent this kind of dependency injection.


Setting Up The Routes
---------------------

Finally we have code which should look pretty familiar at this point throughout the tutorials.  We build our :term:`Route`\s:

.. code:: python

    routes = \
        RoutesBuilder() \
            .add_request_interceptor("/", request_session_building_interceptor.load_session_onto_request) \
            .add_handler("GET", "/messages", messages_handler.get_user_messages) \
            .build()

The only reason to call attention to it here is so that you see how the function assignment works with
:term:`Interceptor`\s and :term:`Handler`\s which have been encapsulated into classes.

