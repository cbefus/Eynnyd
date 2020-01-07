import unittest
import arrow

from eynnyd.internal.utils.cookies.request_cookie import RequestCookie
from eynnyd.response_cookie_builder import ResponseCookieBuilder
from eynnyd.internal.utils.cookies.header_converter import CookieHeaderConverter
from eynnyd.exceptions import InvalidCookieHeaderException


class TestHeaderConverter(unittest.TestCase):

    def test_split_from_header(self):
        cookies = CookieHeaderConverter.from_header("foo=bar;123=456;foo=pants")
        self.assertEqual(2, len(cookies.keys()))
        self.assertTrue("foo" in cookies)
        self.assertEqual([RequestCookie("foo", "bar"), RequestCookie("foo", "pants")], cookies["foo"])
        self.assertTrue("123" in cookies)
        self.assertEqual([RequestCookie("123", "456")], cookies["123"])

    def test_raise_on_bad_name(self):
        with self.assertRaises(InvalidCookieHeaderException):
            CookieHeaderConverter.from_header("f oo=bar")

    def test_raise_on_bad_value(self):
        with self.assertRaises(InvalidCookieHeaderException):
            CookieHeaderConverter.from_header("foo=ba,r")

    def test_from_basic_cookie(self):
        set_header = CookieHeaderConverter.from_cookie(ResponseCookieBuilder("boo", "far").build())
        self.assertEqual(("Set-Cookie", "boo=far; Secure; HttpOnly"), set_header)

    def test_non_secure_cookie(self):
        set_header = \
            CookieHeaderConverter.from_cookie(ResponseCookieBuilder("boo", "far").set_secure(False).build())
        self.assertEqual(("Set-Cookie", "boo=far; HttpOnly"), set_header)

    def test_non_httponly_cookie(self):
        set_header = \
            CookieHeaderConverter.from_cookie(ResponseCookieBuilder("boo", "far").set_http_only(False).build())
        self.assertEqual(("Set-Cookie", "boo=far; Secure"), set_header)

    def test_expires_cookie(self):
        example_expire = arrow.utcnow()
        set_header = \
            CookieHeaderConverter\
                .from_cookie(
                    ResponseCookieBuilder("boo", "far")
                        .set_expires(str(example_expire))
                        .build())
        self.assertEqual(
            (
                "Set-Cookie",
                "boo=far; Expires={f} GMT; Secure; HttpOnly"
                    .format(f=example_expire.format("ddd, DD MMM YYYY HH:MM:SS"))
            ),
            set_header)

    def test_max_age_cookie(self):
        set_header = \
            CookieHeaderConverter\
                .from_cookie(
                    ResponseCookieBuilder("boo", "far")
                        .set_max_age(123)
                        .build())
        self.assertEqual(("Set-Cookie", "boo=far; Max-Age=123; Secure; HttpOnly"), set_header)

    def test_domain_cookie(self):
        set_header = \
            CookieHeaderConverter\
                .from_cookie(
                    ResponseCookieBuilder("boo", "far")
                        .set_domain("localhost")
                        .build())
        self.assertEqual(("Set-Cookie", "boo=far; Domain=localhost; Secure; HttpOnly"), set_header)

    def test_path_cookie(self):
        set_header = \
            CookieHeaderConverter\
                .from_cookie(
                    ResponseCookieBuilder("boo", "far")
                        .set_path("foo/123")
                        .build())
        self.assertEqual(("Set-Cookie", "boo=far; Path=foo/123; Secure; HttpOnly"), set_header)
