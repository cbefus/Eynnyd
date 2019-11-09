from src.internal.wsgi.stream_reader_factory import StreamReaderFactory
from src.internal.wsgi.wsgi_response import WSGIResponse
from src.internal.utils.cookies.header_converter import CookieHeaderConverter
from src.internal.wsgi.wsgi_response_body_factory import WSGIResponseBodyFactory


class WSGIResponseAdapter:

    def __init__(self, wsgi_file_wrapper):
        self._wsgi_file_wrapper = wsgi_file_wrapper

    def adapt(self, response):
        headers = [(str(k), str(v)) for k, v in response.headers.items()]
        headers += [CookieHeaderConverter.from_cookie(cookie) for cookie in response.cookies]

        return WSGIResponse(
            response.status.wsgi_format,
            headers,
            WSGIResponseBodyFactory(
                StreamReaderFactory.create_reader(self._wsgi_file_wrapper))
                    .create(response.body)
                        .get_body())

