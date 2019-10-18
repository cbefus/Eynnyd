from http import HTTPStatus
from abc import ABC, abstractmethod
from enum import Enum

from src.exceptions import InvalidResponseCookieException
from src.exceptions import InvalidHeaderException
from src.exceptions import InvalidBodyTypeException
from src.utils.http_status import HTTPStatusFactory
from src.utils.cookies.cookie import ResponseCookie


class ResponseBodyType(Enum):
    EMPTY = 1
    UTF8 = 2
    BYTE = 3
    STREAM = 4
    ITERABLE = 5


class ResponseBody:

    def __init__(self, type, content):
        self._type = type
        self._content = content

    @staticmethod
    def empty_response():
        return ResponseBody(ResponseBodyType.EMPTY, "")

    @property
    def type(self):
        return self._type

    @property
    def content(self):
        return self._content


class AbstractResponse(ABC):

    @property
    @abstractmethod
    def status(self):
        pass

    @property
    @abstractmethod
    def body(self):
        pass

    @property
    @abstractmethod
    def headers(self):
        pass

    @property
    @abstractmethod
    def cookies(self):
        pass


class Response(AbstractResponse):

    def __init__(self, status, body, headers, cookies):
        self._status = status
        self._body = body
        self._headers = headers
        self._cookies = cookies

    @property
    def status(self):
        return self._status

    @property
    def body(self):
        return self._body

    @property
    def headers(self):
        return self._headers

    @property
    def cookies(self):
        return self._cookies

    def __str__(self):
        return "<{c}>".format(c=self.status)


class ResponseBuilder:

    def __init__(self):
        self._status = HTTPStatusFactory.create(HTTPStatus.OK)
        self._body = ResponseBody.empty_response()
        self._headers = {}
        self._cookies = []

    def set_status(self, status):
        self._status = HTTPStatusFactory.create(status)
        return self

    def set_utf8_body(self, body):
        encoded_body = body.encode("utf-8")
        if len(body) != len(encoded_body):
            raise InvalidBodyTypeException("Body must be UTF8 to set via set_utf8_body method.")
        if "content-length" not in self._headers:
            self._headers["content-length"] = str(len(encoded_body))
        self._body = ResponseBody(ResponseBodyType.UTF8, encoded_body)
        return self

    def set_byte_body(self, body):
        if not isinstance(body, bytes):
            raise InvalidBodyTypeException("Body must be byte encoded to set via set_byte_body mothod.")
        if "content-length" not in self._headers:
            self._headers["content-length"] = str(len(body))
        self._body = ResponseBody(ResponseBodyType.BYTE, body)
        return self

    def set_stream_body(self, body):
        if not hasattr(body, "read"):
            raise InvalidBodyTypeException("Streamable body must have a read method.")
        self._body = ResponseBody(ResponseBodyType.STREAM, body)
        return self

    def set_iterable_body(self, body):
        try:
            iterator = iter(body)
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

        self._headers[ascii_lowered_name] = str(value).lower()
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

    def add_basic_cookie(self,  name, value):
        self._cookies.append(ResponseCookie.build_basic(name, value))
        return self

    def build(self):
        return Response(
            self._status,
            self._body,
            self._headers,
            self._cookies)
