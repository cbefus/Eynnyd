from unittest import TestCase

from eynnyd.internal.response import Response


class TestResponse(TestCase):

    def test_string_repr(self):
        response = Response(200, "", [], [])
        self.assertEqual("<200>", str(response))
