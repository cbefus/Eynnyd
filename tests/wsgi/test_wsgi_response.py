from unittest import TestCase

from eynnyd.internal.wsgi.wsgi_response import WSGIResponse


class TestWSGIResponse(TestCase):

    def test_wsgi_response_properties(self):
        response = WSGIResponse("200 OK", [("foo", "bar"), ("fizz", "buzz")], "cool beans")
        self.assertEqual("200 OK", response.status)
        self.assertListEqual([("foo", "bar"), ("fizz", "buzz")], response.headers)
        self.assertEqual("cool beans", response.body)


