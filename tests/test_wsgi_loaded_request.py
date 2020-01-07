from unittest import TestCase

from eynnyd.internal.wsgi_loaded_request import WSGILoadedRequest
from eynnyd.internal.utils.cookies.request_cookie import RequestCookie


class TestWSGILoadedRequest(TestCase):

    def test_copy_and_set_path_parameters(self):
        original = WSGILoadedRequest({"REQUEST_METHOD": "GET"})
        copy = original.copy_and_set_path_parameters({"pants": "awesome"})
        self.assertDictEqual({"pants": "awesome"}, copy.path_parameters)
        self.assertEqual(original.http_method, copy.http_method)

    def test_http_method(self):
        request = WSGILoadedRequest({"REQUEST_METHOD": "GET"})
        self.assertEqual("GET", request.http_method)

    def test_request_uri(self):
        request = \
            WSGILoadedRequest({
                "wsgi.url_scheme": "https",
                "SERVER_NAME": "localhost",
                "SERVER_PORT": 8008,
                "PATH_INFO": "/foo/bar",
                "QUERY_STRING": "foo=bar&fizz=buzz"
            })
        self.assertEqual("https", request.request_uri.scheme)
        self.assertEqual("localhost", request.request_uri.host)
        self.assertEqual(8008, request.request_uri.port)
        self.assertEqual("/foo/bar", request.request_uri.path)
        self.assertEqual("foo=bar&fizz=buzz", request.request_uri.query)

    def test_forwarded_request_uri(self):
        request = \
            WSGILoadedRequest({
                "wsgi.url_scheme": "https",
                "SERVER_NAME": "localhost",
                "SERVER_PORT": 8008,
                "PATH_INFO": "/foo/bar",
                "QUERY_STRING": "foo=bar&fizz=buzz",
                "HTTP_X_FORWARDED_PROTO": "http",
                "HTTP_X_FORWARDED_HOST": "100.100.100.100"
            })
        self.assertEqual("http", request.forwarded_request_uri.scheme)
        self.assertEqual("100.100.100.100", request.forwarded_request_uri.host)
        self.assertEqual(8008, request.forwarded_request_uri.port)
        self.assertEqual("/foo/bar", request.forwarded_request_uri.path)
        self.assertEqual("foo=bar&fizz=buzz", request.forwarded_request_uri.query)

    def test_headers(self):
        request = \
            WSGILoadedRequest({
                "HTTP_PANTS_ARE_COOL": "THEY sure Are Cap.",
                "CONTENT_LENGTH": 16,
                "CONTENT_TYPE": "application/json",
                "SOMETHING_ELSE": "pffft"
            })
        self.assertDictEqual(
            {
                "PANTS-ARE-COOL": "THEY sure Are Cap.",
                "CONTENT-LENGTH": 16,
                "CONTENT-TYPE": "application/json",
            },
            request.headers)

    def test_client_ip_address(self):
        request =\
            WSGILoadedRequest({"REMOTE_ADDR": "100.100.100.100"})
        self.assertEqual("100.100.100.100", request.client_ip_address)

    def test_cookies(self):
        request =\
            WSGILoadedRequest({
                "HTTP_COOKIE": "foo=bar;fizz=buzz;foo=pants"
            })
        self.assertDictEqual(
            {
                "foo": [RequestCookie("foo", "bar"), RequestCookie("foo", "pants")],
                "fizz": [RequestCookie("fizz", "buzz")]
            },
            request.cookies
        )

    def test_query_parameters(self):
        request =\
            WSGILoadedRequest({
                "QUERY_STRING": "foo=bar&fizz=buzz&foo=pants"
            })
        self.assertDictEqual(
            {
                "foo": ["bar", "pants"],
                "fizz": ["buzz"]
            },
            request.query_parameters
        )

    def test_byte_body(self):

        class FakeBody:
            def read(self, size):
                return b"some body content"

        request =\
            WSGILoadedRequest({
                "CONTENT_LENGTH": 20,
                "wsgi.input": FakeBody()
            })
        self.assertEqual(b"some body content", request.byte_body)

    def test_byte_body_no_length(self):

        class SpyBody:
            def __init__(self):
                self._size = 22

            @property
            def size(self):
                return self._size

            def read(self, size):
                self._size = size
                return b""
        body = SpyBody()
        request =\
            WSGILoadedRequest({
                "CONTENT_LENGTH": "booots",
                "wsgi.input": body
            })
        self.assertEqual(b"", request.byte_body)
        self.assertEqual(0, body.size)

    def test_utf8_body(self):
        class FakeBody:
            def read(self, size):
                return b"some body content"

        request =\
            WSGILoadedRequest({
                "CONTENT_LENGTH": 20,
                "wsgi.input": FakeBody()
            })
        self.assertEqual("some body content", request.utf8_body)

    def test_string_repr(self):
        request =\
            WSGILoadedRequest({
                "REQUEST_METHOD": "GET",
                "wsgi.url_scheme": "https",
                "SERVER_NAME": "localhost",
                "SERVER_PORT": 8008,
                "PATH_INFO": "/foo/bar",
                "QUERY_STRING": "foo=bar&fizz=buzz"
            })
        self.assertEqual(
            "<GET https://localhost:8008/foo/bar?foo=bar&fizz=buzz>",
            str(request)
        )





