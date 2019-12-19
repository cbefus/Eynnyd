.. _glossary:

Glossary
========

Throughout these docs and our code we use a series of terms which we hope make sense inherently but just in case we
have compiled this glossary:

.. glossary::
    Handler
        A Handler is the code executed for a request which converts a request into a response. In Eynnyd it
        is simply a function which takes a single argument (the request) and returns a response.

    Interceptor
        An Interceptor is code which is executed before or after a :term:`Handler` for a request.  Request
        Interceptors happen before the :term:`Handler` and Response Interceptors happen after.  In Eynnyd
        you can have as many Interceptors as you like executed around a :term:`Handler`.  In some frameworks
        this is also called Middleware.

    Route
        A route is a path of execution to some code.  :term:`Handler` Routes use an HTTP method like "GET", "POST",
        "PUT", "DELETE", etc., and a path like "/foo/bar" to decide what handlers to execute.  :term:`Interceptor`
        Routes only require a path and execute for every request along that path.

    Error Handler
        An Error Handler is code that gets executed when an associated exception is thrown.  There are two types of
        pre response error handlers and post response error handler. Pre response error handlers which execute when
        an exception is thrown from a request :term:`Interceptor` or a :term:`Handler`. Post response error handlers
        execute when an exception is thrown during response :term:`Interceptor`\s.

