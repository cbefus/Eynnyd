from http import HTTPStatus

from eynnyd.internal.utils.http_status_factory import HTTPStatusFactory


class RawWSGIServerErrorResponse:

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