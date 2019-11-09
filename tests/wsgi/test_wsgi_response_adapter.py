from unittest import TestCase
from http import HTTPStatus

from src.internal.wsgi.wsgi_response_adapter import WSGIResponseAdapter
from src.response_builder import ResponseBuilder


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
        self.assertListEqual(
            [
                ("foo", "bar"),
                ("fizz", "buzz"),
                ('content-length', '15'),
                ('Set-Cookie', 'pants=shirt; Secure; HttpOnly')
            ],
            wsgi_response.headers
        )
        self.assertListEqual([b"foobar-fizzbuzz"], list(wsgi_response.body))










