from unittest import TestCase

from eynnyd.internal.wsgi.raw_wsgi_server_error_response import RawWSGIServerErrorResponse


class TestRawWSGIServerErrorResponse(TestCase):

    def test_server_error_response_properties(self):
        response = RawWSGIServerErrorResponse()
        self.assertEqual("500 INTERNAL_SERVER_ERROR", response.status)
        self.assertListEqual([], response.headers)
        self.assertListEqual(["500 Internal Server Error".encode("utf-8")], response.body)



