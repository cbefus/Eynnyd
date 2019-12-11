.. _deploy:

Deploy
======

Eynnyd is a `WSGI <https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface>`__ framework, which means to
serve an Eynnyd application you need to run a WSGI server.  We recommend `Gunicorn <https://gunicorn.org/>`__
(as it is what we use) but there are many worth looking into.

Local Serving
-------------
If you used Gunicorn then you can run your application via:

.. code:: bash

    gunicorn hello_world_app

This assumes that you have a file named *hellow_world_app.py* where inside you have a variable named
*application* which returns the built Eynnyd Webapp (See :ref:`the hello world tutorial <hello_world>`
for an example).

Deploying a Server
------------------
Due to Eynnyd being a new framework we don't have a ton of documentation on deploying to various cloud systems.

The good news is that because it is a WSGI framework, Eynnyd can be used as a drop in replacement for any
tutorial on how to deploy any other WSGI frameworks.

Keep watching though for coming documentation on deploying Eynnyd specifically.
