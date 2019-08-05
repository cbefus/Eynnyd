from http import HTTPStatus
from src.utils.http_status import HTTPStatusFactory


class WSGIResponse:

    def __init__(self, status, headers, body):
        self._status = status
        self._headers = headers
        self._body = body

    @property
    def status(self):
        return self._status

    @property
    def headers(self):
        return self._headers

    @property
    def body(self):
        return self._body


class RawWSGIServerError:

    @property
    def status(self):
        return HTTPStatusFactory\
            .create(HTTPStatus.INTERNAL_SERVER_ERROR)\
            .wsgi_format

    @property
    def headers(self):
        return []

    @property
    def body(self):
        return ["500 Internal Server Error".encode("utf-8")]
