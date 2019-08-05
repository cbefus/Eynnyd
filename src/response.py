from http import HTTPStatus

from src.utils.http_status import HTTPStatusFactory
from src.abstract_response import AbstractResponse


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
        #  TODO: Validation
        self._headers = headers_by_name
        return self

    def add_header(self, name, value):
        #  TODO: Validation
        self._headers[name] = value
        return self

    def set_cookies(self, cookies):
        #  TODO: Validation
        self._cookies = cookies
        return self

    def add_cookie(self, cookie):
        #  TODO: Validation
        self._cookies.append(cookie)
        return self

    def build(self):
        return Response(
            self._status,
            self._body,
            self._headers,
            self._cookies)


class ResponseBuildException(Exception):
    pass