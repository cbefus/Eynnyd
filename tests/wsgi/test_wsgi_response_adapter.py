from unittest import TestCase
from http import HTTPStatus

from eynnyd.internal.wsgi.wsgi_response_adapter import WSGIResponseAdapter
from eynnyd.response_builder import ResponseBuilder


class TestWSGIResponseAdapter(TestCase):

    def test_adapt(self):
        response = \
            ResponseBuilder()\
                .set_status(HTTPStatus.CREATED)\
                .add_header("foo", "bar")\
                .add_header("fizz", "buzz")\
                .add_basic_cookie("pants", "shirt")\
                .set_utf8_body("foobar-fizzbuzz")\
                .build()
        wsgi_response = WSGIResponseAdapter(None).adapt(response)
        self.assertEqual("201 CREATED", wsgi_response.status)
        self.assertEqual(4, len(wsgi_response.headers))
        self.assertTrue(("foo", "bar") in wsgi_response.headers)
        self.assertTrue(("fizz", "buzz") in wsgi_response.headers)
        self.assertTrue(('content-length', '15') in wsgi_response.headers)
        self.assertTrue(('Set-Cookie', 'pants=shirt; Secure; HttpOnly') in wsgi_response.headers)
        self.assertEqual(1, len(list(wsgi_response.body)))
        self.assertTrue(b"foobar-fizzbuzz" in list(wsgi_response.body))










