from unittest import TestCase

from eynnyd.internal.wsgi.utf8_response_body import UTF8ResponseBody


class TestUTF8ResponseBody(TestCase):

    def test_get_body(self):
        body = UTF8ResponseBody("foobar")
        self.assertListEqual(["foobar"], body.get_body())

