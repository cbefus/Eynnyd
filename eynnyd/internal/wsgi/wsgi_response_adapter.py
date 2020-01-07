from eynnyd.internal.wsgi.wsgi_response import WSGIResponse
from eynnyd.internal.utils.cookies.header_converter import CookieHeaderConverter
from eynnyd.internal.wsgi.wsgi_response_body_factory import WSGIResponseBodyFactory


class WSGIResponseAdapter:

    def __init__(self, stream_reader):
        self._stream_reader = stream_reader

    def adapt(self, response):
        headers = [(str(k), str(v)) for k, v in response.headers.items()]
        headers += [CookieHeaderConverter.from_cookie(cookie) for cookie in response.cookies]

        return WSGIResponse(
            response.status.wsgi_format,
            headers,
            WSGIResponseBodyFactory(self._stream_reader).create(response.body).get_body())

