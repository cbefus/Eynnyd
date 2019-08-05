
# Eynnyd WebServer
Eynnyd (pronounced [Ey-nahyd]) is an acronym for **Everything You Need, Nothing
You Don't**. It is a light-weight WSGI compliant python 3 web server framework.
Eynnyd was designed with the primary goal to not impose bad engineering decisions
on it's users. It is also designed to not overstep or assume the wants of it's user.

#### Simplicity and Freedom is the Design
This is the framework for you if the following sound good:
* A `request interceptor` takes a `request` and returns a `request`.
* A `request handler` takes a `request` and returns a `response`.
* A `response interceptor` takes a `response` and returns a `response`.
* You can have any number of request interceptors.
* You can have any number of request handlers.
* You can have any number of response interceptors.
* You are permitted but not coerced into following REST.
* We do not provide extraneous dependencies or opinions (like database connection libraries or templating engine)
* There is no _Eynnyd way_ to do things.
* There is nothing _clever_ or _magic_. (like global singletons or special decorators)
* You can see your entire routing layout in your main.

If this at all sounds we recommend you keep reading and see what else Eynnyd
can provide for you.

## How to use it
Eynnyd does not come with a built in WSGI HTTP server. We recommend
[gunicorn](https://gunicorn.org/) for running your application.

A simple hello world example looks like:
```
# hello_world_app.py
from eynnyd import RoutesBuilder
from eynnyd import EynnydWebappBuilder
from eynnyd import ResponseBuilder
from http import HTTPStatus

def hello_world(request):
    return ResponseBuilder()\
        .set_status(HTTPStatus.OK)\
        .set_body("Hello World")\
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
```
Using gunicorn this can now be run `gunicorn hello_world_app`.

### A slightly fancier example
coming soon.

## Notes
Must use python >3.2 (functools.lru_cache())
