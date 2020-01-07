from unittest import TestCase

from eynnyd.internal.utils.http_status import HTTPStatus


class TestHTTPStatus(TestCase):

    def test_http_status_str(self):
        status = HTTPStatus(400, "bad request", "generically bad request")
        self.assertEqual("400 bad request", str(status))

    def test_http_status_wsgi_format(self):
        status = HTTPStatus(400, "bad request", "generically bad request")
        self.assertEqual("400 bad request", status.wsgi_format)

    def test_http_status_properties(self):
        status = HTTPStatus(400, "bad request", "generically bad request")
        self.assertEqual(400, status.code)
        self.assertEqual("bad request", status.phrase)
        self.assertEqual("generically bad request", status.description)
