from unittest import TestCase
from http import HTTPStatus as HTTPLibHTTPStatus

from eynnyd.exceptions import SettingNonTypedStatusWithContentTypeException, SettingNonBodyStatusWithBodyException, \
    SettingBodyWithNonBodyStatusException, InvalidBodyTypeException, InvalidHeaderException, \
    SettingContentTypeWithNonTypedStatusException, InvalidResponseCookieException
from eynnyd.response_builder import ResponseBuilder
from eynnyd.internal.response_body_type import ResponseBodyType
from eynnyd.response_cookie_builder import ResponseCookieBuilder


class TestResponseBuilder(TestCase):

    def test_set_status_raise_on_content_type_response_with_non_content_status(self):
        builder = ResponseBuilder().add_header("content-type", "application/json")
        with self.assertRaises(SettingNonTypedStatusWithContentTypeException):
            builder.set_status(builder.set_status(HTTPLibHTTPStatus.NO_CONTENT))

    def test_set_status_raise_on_body_response_with_non_body_status(self):
        builder = ResponseBuilder().set_utf8_body("foobar")
        with self.assertRaises(SettingNonBodyStatusWithBodyException):
            builder.set_status(builder.set_status(HTTPLibHTTPStatus.NO_CONTENT))

    def test_set_status(self):
        response = ResponseBuilder().set_status(HTTPLibHTTPStatus.CREATED).build()
        self.assertEqual(HTTPLibHTTPStatus.CREATED.value, response.status.code)

    def test_set_utf8_body_raises_on_non_body_status(self):
        builder = ResponseBuilder().set_status(HTTPLibHTTPStatus.NO_CONTENT)
        with self.assertRaises(SettingBodyWithNonBodyStatusException):
            builder.set_utf8_body("foobar")

    def test_set_utf8_body_raises_on_non_utf8_body(self):
        with self.assertRaises(InvalidBodyTypeException):
            ResponseBuilder().set_utf8_body("fooć𝗱ễbar")

    def test_set_utf8_body(self):
        response = ResponseBuilder().set_utf8_body("foobar fizzbuzz 1234").build()
        self.assertEqual(b"foobar fizzbuzz 1234", response.body.content)
        self.assertEqual("20", response.headers["content-length"])

    def test_set_byte_body_raises_on_non_body_status(self):
        builder = ResponseBuilder().set_status(HTTPLibHTTPStatus.NO_CONTENT)
        with self.assertRaises(SettingBodyWithNonBodyStatusException):
            builder.set_byte_body(b"foobar")

    def test_set_byte_body_raises_on_non_byte_body(self):
        with self.assertRaises(InvalidBodyTypeException):
            ResponseBuilder().set_byte_body("not a byte body")

    def test_set_byte_body(self):
        response = ResponseBuilder().set_byte_body(b"foobar fizzbuzz 1234").build()
        self.assertEqual(b"foobar fizzbuzz 1234", response.body.content)
        self.assertEqual("20", response.headers["content-length"])

    def test_set_stream_body_raises_on_non_body_status(self):
        class FakeBody:
            def read(self, size):
                pass
        builder = ResponseBuilder().set_status(HTTPLibHTTPStatus.NO_CONTENT)
        with self.assertRaises(SettingBodyWithNonBodyStatusException):
            builder.set_stream_body(FakeBody())

    def test_set_stream_body_raises_without_read_method(self):
        class FakeBody:
            pass
        with self.assertRaises(InvalidBodyTypeException):
            ResponseBuilder().set_stream_body(FakeBody())

    def test_set_stream_body_raises_without_read_method_taking_a_single_param(self):
        class FakeBody:
            def read(self):
                pass
        with self.assertRaises(InvalidBodyTypeException):
            ResponseBuilder().set_stream_body(FakeBody())

    def test_set_stream_body(self):
        class FakeBody:
            def read(self, size):
                return b"stuff"
        response = ResponseBuilder().set_stream_body(FakeBody()).build()
        self.assertEqual(ResponseBodyType.STREAM, response.body.type)

    def test_set_iterable_raises_on_non_body_status(self):
        builder = ResponseBuilder().set_status(HTTPLibHTTPStatus.NO_CONTENT)
        with self.assertRaises(SettingBodyWithNonBodyStatusException):
            builder.set_iterable_body(["foobar"])

    def test_set_iterable_raises_on_not_iterable_type(self):
        with self.assertRaises(InvalidBodyTypeException):
            ResponseBuilder().set_iterable_body(123)

    def test_set_iterable(self):
        response = ResponseBuilder().set_iterable_body(["foobar"]).build()
        self.assertEqual(ResponseBodyType.ITERABLE, response.body.type)

    def test_unset_body(self):
        response = ResponseBuilder().set_utf8_body("foobar").unset_body().build()
        self.assertEqual(ResponseBodyType.EMPTY, response.body.type)

    def test_set_headers(self):
        response = ResponseBuilder().set_headers({"foo": "bar"}).build()
        self.assertDictEqual({"foo": "bar"}, response.headers)

    def test_add_header_raises_on_a_cookie_header(self):
        with self.assertRaises(InvalidHeaderException):
            ResponseBuilder().add_header("set-cookie", "foobar")

    def test_add_header_raises_on_contet_type_header_with_non_content_status(self):
        builder = ResponseBuilder().set_status(HTTPLibHTTPStatus.NO_CONTENT)
        with self.assertRaises(SettingContentTypeWithNonTypedStatusException):
            builder.add_header("content-type", "foobar")

    def test_add_header(self):
        response = ResponseBuilder().add_header("FOObar", "FizzBuzz").build()
        self.assertDictEqual(
            {
                "foobar": "FizzBuzz"
            },
            response.headers)

    def test_remove_header(self):
        response = ResponseBuilder().add_header("FOObar", "FizzBuzz").remove_header("fooBAR").build()
        self.assertDictEqual({}, response.headers)

    def test_setting_cookies_with_non_cookie_raises(self):
        with self.assertRaises(InvalidResponseCookieException):
            ResponseBuilder().set_cookies(["boom"])

    def test_setting_cookies(self):
        response = ResponseBuilder().set_cookies([ResponseCookieBuilder("foo", "bar").build()]).build()
        self.assertListEqual([ResponseCookieBuilder("foo", "bar").build()], response.cookies)

    def test_add_cookie_raises_with_non_cookie(self):
        with self.assertRaises(InvalidResponseCookieException):
            ResponseBuilder().add_cookie("boom")

    def test_add_cookie(self):
        response = ResponseBuilder().add_cookie(ResponseCookieBuilder("foo", "bar").build()).build()
        self.assertListEqual([ResponseCookieBuilder("foo", "bar").build()], response.cookies)

    def test_add_basic_cookie(self):
        response = ResponseBuilder().add_basic_cookie("foo", "bar").build()
        self.assertListEqual([ResponseCookieBuilder("foo", "bar").build()], response.cookies)

    def test_remove_cookie(self):
        response = ResponseBuilder().add_basic_cookie("foo", "bar").remove_cookie("foo").build()
        self.assertListEqual([], response.cookies)







