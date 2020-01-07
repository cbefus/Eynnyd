import unittest
import arrow

from eynnyd.response_cookie_builder import ResponseCookieBuilder
from eynnyd.exceptions import InvalidCookieBuildException


class TestResponseCookieBuilder(unittest.TestCase):

    def test_default_cookie(self):
        cookie = ResponseCookieBuilder("foo", "bar").build()
        self.assertEqual("foo", cookie.name)
        self.assertEqual("bar", cookie.value)
        self.assertTrue(cookie.expires.is_empty())
        self.assertTrue(cookie.max_age.is_empty())
        self.assertTrue(cookie.domain.is_empty())
        self.assertTrue(cookie.path.is_empty())
        self.assertTrue(cookie.secure)
        self.assertTrue(cookie.http_only)

    def test_raises_on_name_error(self):
        with self.assertRaises(InvalidCookieBuildException):
            ResponseCookieBuilder("f@oo", "bar").build()

    def test_raises_on_value_error(self):
        with self.assertRaises(InvalidCookieBuildException):
            ResponseCookieBuilder("foo", "b a r").build()

    def test_cookie_with_expires(self):
        example_expire = str(arrow.utcnow())
        cookie = \
            ResponseCookieBuilder("foo", "bar") \
                .set_expires(example_expire) \
                .build()
        self.assertTrue(cookie.expires.is_present())
        self.assertEqual(arrow.get(example_expire), cookie.expires.get())

    def test_cookie_with_expires_raises_on_bad_date(self):
        with self.assertRaises(InvalidCookieBuildException):
            ResponseCookieBuilder("foo", "bar") \
                .set_expires("bad date") \
                .build()

    def test_cookie_with_expires_in_days(self):
        shifted_before = arrow.utcnow().shift(days=5)
        cookie = \
            ResponseCookieBuilder("foo", "bar") \
                .set_expires_in_days(5) \
                .build()
        shifted_after = arrow.utcnow().shift(days=5)
        self.assertTrue(cookie.expires.is_present())
        self.assertTrue(
            cookie.expires.get().is_between(shifted_before, shifted_after),
            msg="{e} is not > than {b} and < {a}".format(e=cookie.expires.get(), b=shifted_before, a=shifted_after))

    def test_raises_with_bad_expiry_days(self):
        with self.assertRaises(InvalidCookieBuildException):
            ResponseCookieBuilder("foo", "bar") \
                .set_expires_in_days("boo") \
                .build()

    def test_set_max_age(self):
        cookie = \
            ResponseCookieBuilder("foo", "bar") \
                .set_max_age(3) \
                .build()
        self.assertTrue(cookie.max_age.is_present())
        self.assertEqual("3", cookie.max_age.get())

    def test_raises_on_bad_max_age(self):
        with self.assertRaises(InvalidCookieBuildException):
            ResponseCookieBuilder("foo", "bar")\
                .set_max_age(0)\
                .build()

    def test_set_domain(self):
        cookie = \
            ResponseCookieBuilder("foo", "bar") \
                .set_domain("localhost")\
                .build()
        self.assertTrue(cookie.domain.is_present())
        self.assertEqual("localhost", cookie.domain.get())

    def test_raises_on_bad_domain(self):
        with self.assertRaises(InvalidCookieBuildException):
            ResponseCookieBuilder("foo", "bar") \
                .set_domain("--")\
                .build()

    def test_set_path(self):
        cookie = \
            ResponseCookieBuilder("foo", "bar") \
                .set_path("abc/123")\
                .build()
        self.assertTrue(cookie.path.is_present())
        self.assertEqual("abc/123", cookie.path.get())

    def test_raises_on_bad_path(self):
        with self.assertRaises(InvalidCookieBuildException):
            ResponseCookieBuilder("foo", "bar") \
                .set_path("\n\t") \
                .build()

    def test_set_secure(self):
        cookie = \
            ResponseCookieBuilder("foo", "bar") \
                .set_secure(False) \
                .build()
        self.assertFalse(cookie.secure)

    def test_set_http_only(self):
        cookie = \
            ResponseCookieBuilder("foo", "bar") \
                .set_http_only(False) \
                .build()
        self.assertFalse(cookie.http_only)
