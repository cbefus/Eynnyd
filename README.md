[![Build Status](https://img.shields.io/pypi/v/eynnyd.svg)](https://pypi.org/project/eynnyd/)
[![Build Status](https://travis-ci.com/cbefus/eynnyd.svg?branch=master)](https://travis-ci.com/cbefus/eynnyd)
[![Coverage Status](https://coveralls.io/repos/github/cbefus/Eynnyd/badge.svg?branch=master)](https://coveralls.io/github/cbefus/Eynnyd?branch=master)
[![PyPI - License](https://img.shields.io/pypi/l/eynnyd)](https://pypi.org/project/eynnyd/)
[![Python Versions](https://img.shields.io/pypi/pyversions/eynnyd.svg)](https://pypi.org/project/eynnyd/)
[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.png?v=103)](https://github.com/open-source)
[![Documentation Status](https://readthedocs.org/projects/eynnyd/badge/?version=latest)](https://eynnyd.readthedocs.io/en/latest/?badge=latest)

<div align="center" style="margin-top: -32px!important;margin-bottom: -70px!important;">
    <img
        src="https://raw.githubusercontent.com/cbefus/eynnyd/master/logo/banner.png"
        alt="Eynnyd web framework logo"
        style="width:100%"
    >
</div>

# Eynnyd Web Framework
Eynnyd (pronounced [Ey-nahyd]) is an acronym for **Everything You Need, Nothing
You Don't**. It is a light-weight WSGI compliant python 3 web framework.
Eynnyd was designed with the primary goal to not impose bad engineering decisions
on it's users. It is also designed to not overstep or assume the wants of it's user.

#### Simplicity and Freedom is the Design
This is the framework for you if the following sound good:
* You are permitted but not coerced into following REST.
* A `request handler` takes a `request` and returns a `response`.
* A `request interceptor` takes a `request` and returns a `request`.
* A `response interceptor` takes a `request` and a `response` and returns a `response`.
* You can have any number of `request interceptors`, `request handlers`, or `response interceptors`.
* You can name your handler methods anything you want.
* You can limit the scope (paths it applies to) of any interceptor.
* We do not provide extraneous dependencies or opinions (like database connection libraries or templating engines)
* There is no _Eynnyd way_ to do things.
* There is nothing _clever_ or _magic_. (like global singletons or special decorators)
* You can see your entire routing layout, succinctly, in your main.

If this at all sounds good we recommend you keep reading and see what else Eynnyd
can provide for you.

## Documents
Read the documents at [eynnyd.readthedocs.io](https://eynnyd.readthedocs.io/en/latest)

## How to install it
Eynnyd is published to pypi and can be installed using:
```bash
pip install eynnyd
```

## How to use it
Eynnyd does not come with a built in WSGI HTTP server. We recommend
[gunicorn](https://gunicorn.org/) for running your application.

A simple hello world example looks like:
```python
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
```
Using gunicorn this can now be run `gunicorn hello_world_app`.

### An example with interceptors

```python
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

def log_response(request, response):
    LOG.info("Built Response: {s} for Request: {r}".format(s=response, r=request))
    return response

def build_application():
    routes = \
        RoutesBuilder()\
            .add_request_interceptor("/hello", log_request)\
            .add_handler("GET", "/hello", hello_world)\
            .add_response_interceptor("/hello", log_response)\
            .build()

    return EynnydWebappBuilder()\
            .set_routes(routes)\
            .build()

application = build_application()
```

# For Developers / Contributors

## Installing requirements
run:
```bash
pip install -r test_requirements.txt
```

## Running the tests
After installing the requirements run:
```bash
python -m unittest discover tests
```

## Checking coverage
After installing the requirements run:
```bash
coverage run --source eynnyd/ -m unittest discover tests/
coverage report
```