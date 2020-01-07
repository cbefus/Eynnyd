from unittest import TestCase

from eynnyd.internal.wsgi.iterable_response_body import IterableResponseBody


class TestIterableResponseBody(TestCase):

    def test_get_body(self):
        body = IterableResponseBody(["foo", "bar"])
        self.assertListEqual(["foo", "bar"], body.get_body())

