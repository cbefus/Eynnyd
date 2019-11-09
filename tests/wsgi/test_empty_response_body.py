from unittest import TestCase

from src.internal.wsgi.empty_response_body import EmptyResponseBody


class TestEmptyResponseBody(TestCase):

    def test_get_body(self):
        body = EmptyResponseBody()
        self.assertListEqual([], body.get_body())
