import unittest

from eynnyd.internal.utils.cookies.request_cookie import RequestCookie


class TestRequestCookie(unittest.TestCase):

    def test_properties(self):
        cookie = RequestCookie("foo", "bar")
        self.assertEqual("foo", cookie.name)
        self.assertEqual("bar", cookie.value)

