from unittest import TestCase

from eynnyd.internal.utils.request_uri import RequestURI


class TestRequestURI(TestCase):

    def test_request_uri_properties(self):
        request_uri = RequestURI("http", "localhost", 8008, "/foo/bar", "foo=bar&fizz=buzz")
        self.assertEqual("http", request_uri.scheme)
        self.assertEqual("localhost", request_uri.host)
        self.assertEqual(8008, request_uri.port)
        self.assertEqual("/foo/bar", request_uri.path)
        self.assertEqual("foo=bar&fizz=buzz", request_uri.query)

    def test_properties_from_wsgi_environment(self):
        request_uri = \
            RequestURI.from_wsgi_environment({
                "wsgi.url_scheme": "http",
                "SERVER_NAME": "localhost",
                "SERVER_PORT": 8008,
                "PATH_INFO": "/foo/bar",
                "QUERY_STRING": "foo=bar&fizz=buzz"
            })
        self.assertEqual("http", request_uri.scheme)
        self.assertEqual("localhost", request_uri.host)
        self.assertEqual(8008, request_uri.port)
        self.assertEqual("/foo/bar", request_uri.path)
        self.assertEqual("foo=bar&fizz=buzz", request_uri.query)

    def test_properties_from_forwarded_from_wsgi_environment_without_forward_headers(self):
        request_uri = \
            RequestURI.forwarded_from_wsgi_environment({
                "wsgi.url_scheme": "http",
                "SERVER_NAME": "localhost",
                "SERVER_PORT": 8008,
                "PATH_INFO": "/foo/bar",
                "QUERY_STRING": "foo=bar&fizz=buzz"
            })
        self.assertEqual("http", request_uri.scheme)
        self.assertEqual("localhost", request_uri.host)
        self.assertEqual(8008, request_uri.port)
        self.assertEqual("/foo/bar", request_uri.path)
        self.assertEqual("foo=bar&fizz=buzz", request_uri.query)

    def test_properties_from_forwarded_from_wsgi_environment_with_http_forwarded_headers(self):
        request_uri = \
            RequestURI.forwarded_from_wsgi_environment({
                "wsgi.url_scheme": "http",
                "SERVER_NAME": "localhost",
                "SERVER_PORT": 8008,
                "PATH_INFO": "/foo/bar",
                "QUERY_STRING": "foo=bar&fizz=buzz",
                "HTTP_FORWARDED": "proto=https;host=100.100.100.100"
            })
        self.assertEqual("https", request_uri.scheme)
        self.assertEqual("100.100.100.100", request_uri.host)
        self.assertEqual(8008, request_uri.port)
        self.assertEqual("/foo/bar", request_uri.path)
        self.assertEqual("foo=bar&fizz=buzz", request_uri.query)

    def test_properties_from_forwarded_from_wsgi_environment_with_http_x_forwarded_headers(self):
        request_uri = \
            RequestURI.forwarded_from_wsgi_environment({
                "wsgi.url_scheme": "http",
                "SERVER_NAME": "localhost",
                "SERVER_PORT": 8008,
                "PATH_INFO": "/foo/bar",
                "QUERY_STRING": "foo=bar&fizz=buzz",
                "HTTP_X_FORWARDED_PROTO": "https",
                "HTTP_X_FORWARDED_HOST": "100.100.100.100"
            })
        self.assertEqual("https", request_uri.scheme)
        self.assertEqual("100.100.100.100", request_uri.host)
        self.assertEqual(8008, request_uri.port)
        self.assertEqual("/foo/bar", request_uri.path)
        self.assertEqual("foo=bar&fizz=buzz", request_uri.query)

    def test_uri_string_repr(self):
        request_uri = RequestURI("http", "localhost", 8008, "/foo/bar", "foo=bar&fizz=buzz")
        self.assertEqual("http://localhost:8008/foo/bar?foo=bar&fizz=buzz", str(request_uri))

    def test_uri_repr(self):
        request_uri = RequestURI("http", "localhost", 8008, "/foo/bar", "foo=bar&fizz=buzz")
        self.assertEqual("http://localhost:8008/foo/bar?foo=bar&fizz=buzz", repr(request_uri))

