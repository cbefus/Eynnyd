import inspect
from http import HTTPStatus

from src.exceptions import SettingNonTypedStatusWithContentTypeException, SettingNonBodyStatusWithBodyException, \
    SettingBodyWithNonBodyStatusException, InvalidBodyTypeException, InvalidHeaderException, \
    SettingContentTypeWithNonTypedStatusException, InvalidResponseCookieException
from src.response import Response
from src.response_body import ResponseBody
from src.response_body_type import ResponseBodyType
from src.utils.cookies.response_cookie import ResponseCookie
from src.utils.cookies.response_cookie_builder import ResponseCookieBuilder
from src.utils.http_status_factory import HTTPStatusFactory
from src.utils.http_status_groups import NON_TYPED_STATUSES, NON_BODY_STATUSES


class ResponseBuilder:

    def __init__(self):
        self._status = HTTPStatusFactory.create(HTTPStatus.OK)
        self._body = ResponseBody.empty_response()
        self._headers = {}
        self._cookies = []

    def set_status(self, status):
        if status in NON_TYPED_STATUSES and "content-type" in self._headers:
            raise SettingNonTypedStatusWithContentTypeException(
                "Cannot set status {s} when content-type header exists.".format(s=status))
        if status in NON_BODY_STATUSES and self._body.type != ResponseBodyType.EMPTY:
            raise SettingNonBodyStatusWithBodyException(
                "Cannot set status {s} on response with body".format(s=status))
        self._status = HTTPStatusFactory.create(status)
        return self

    def set_utf8_body(self, body):
        if self._status in NON_BODY_STATUSES:
            raise SettingBodyWithNonBodyStatusException(
                "Cannot set a body on response with status {s}".format(s=self._status))
        encoded_body = body.encode("utf-8")
        if len(body) != len(encoded_body):
            raise InvalidBodyTypeException("Body must be UTF8 to set via set_utf8_body method.")
        if "content-length" not in self._headers:
            self._headers["content-length"] = str(len(encoded_body))
        self._body = ResponseBody(ResponseBodyType.UTF8, encoded_body)
        return self

    def set_byte_body(self, body):
        if self._status in NON_BODY_STATUSES:
            raise SettingBodyWithNonBodyStatusException(
                "Cannot set a body on response with status {s}".format(s=self._status))
        if not isinstance(body, bytes):
            raise InvalidBodyTypeException("Body must be byte encoded to set via set_byte_body mothod.")
        if "content-length" not in self._headers:
            self._headers["content-length"] = str(len(body))
        self._body = ResponseBody(ResponseBodyType.BYTE, body)
        return self

    def set_stream_body(self, body):
        if self._status in NON_BODY_STATUSES:
            raise SettingBodyWithNonBodyStatusException(
                "Cannot set a body on response with status {s}".format(s=self._status))
        if not hasattr(body, "read"):
            raise InvalidBodyTypeException("Streamable body must have a read method.")

        if 1 != len(inspect.signature(body.read).parameters):
            raise InvalidBodyTypeException("Streamable body read method must take a block size parameter")

        self._body = ResponseBody(ResponseBodyType.STREAM, body)
        return self

    def set_iterable_body(self, body):
        if self._status in NON_BODY_STATUSES:
            raise SettingBodyWithNonBodyStatusException(
                "Cannot set a body on response with status {s}".format(s=self._status))
        try:
            iter(body)
        except TypeError as e:
            raise InvalidBodyTypeException("Iterable bodies must be iterable", e)
        self._body = ResponseBody(ResponseBodyType.ITERABLE, body)
        return self

    def unset_body(self):
        self._body = ResponseBody.empty_response()
        return self

    def set_headers(self, headers_by_name):
        self._headers = {}
        for name, value in headers_by_name.items():
            self.add_header(name, value)
        return self

    def add_header(self, name, value):
        ascii_lowered_name = str(name).lower()
        if ascii_lowered_name == 'set-cookie':
            raise InvalidHeaderException("Cannot set header with {n} as name".format(n=name))
        if self._status in NON_TYPED_STATUSES and ascii_lowered_name == 'content-type':
            raise SettingContentTypeWithNonTypedStatusException(
                "Cannot set content-type header on response with status {s}".format(s=self._status))
        self._headers[ascii_lowered_name] = str(value).lower()
        return self

    def remove_header(self, name):
        ascii_lowered_name = str(name).lower()
        if ascii_lowered_name in self._headers:
            self._headers.pop(ascii_lowered_name)
        return self

    def set_cookies(self, cookies):
        for cookie in cookies:
            if not isinstance(cookie, ResponseCookie):
                raise InvalidResponseCookieException("Cookie {c} is not a valid response cookie.".format(c=str(cookie)))
        self._cookies = cookies
        return self

    def add_cookie(self, cookie):
        if not isinstance(cookie, ResponseCookie):
            raise InvalidResponseCookieException("Cookie {c} is not a valid response cookie.".format(c=str(cookie)))
        self._cookies.append(cookie)
        return self

    def add_basic_cookie(self, name, value):
        self._cookies.append(ResponseCookieBuilder(name, value).build())
        return self

    def remove_cookie(self, name):
        self._cookies = filter(lambda cookie: cookie.name != name, self._cookies)

    def build(self):
        return Response(
            self._status,
            self._body,
            self._headers,
            self._cookies)