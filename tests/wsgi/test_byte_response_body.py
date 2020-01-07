from unittest import TestCase

from eynnyd.internal.wsgi.byte_response_body import ByteResponseBody


class TestByteResponseBody(TestCase):

    def test_get_body(self):
        body = ByteResponseBody(b"foobar")
        self.assertListEqual([b"foobar"], body.get_body())
