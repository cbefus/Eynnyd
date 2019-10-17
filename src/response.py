from http import HTTPStatus
from abc import ABC, abstractmethod

from src.exceptions import ResponseBuildException, InvalidResponseCookieException, InvalidHeaderException
from src.utils.http_status import HTTPStatusFactory
from src.utils.cookies.cookie import ResponseCookie


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
        self._body = ""
        self._headers = {}
        self._cookies = []

    def set_status(self, status):
        self._status = HTTPStatusFactory.create(status)
        return self

    def set_body(self, body):
        if not isinstance(body, str):
            raise ResponseBuildException("Cannot set non-string body: {b}".format(b=body))
        self._body = body
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
        if "Content-Length" not in self._headers:
            self._headers["Content-Length"] = str(len(self._body))
        return Response(
            self._status,
            self._body,
            self._headers,
            self._cookies)
