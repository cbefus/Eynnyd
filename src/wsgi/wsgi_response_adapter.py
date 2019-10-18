from abc import ABC, abstractmethod

from src.wsgi.wsgi_response import WSGIResponse
from src.utils.cookies.header_converter import CookieHeaderConverter
from src.response import ResponseBodyType
from src.exceptions import UnknownResponseBodyTypeException
from src.wsgi.closeable_stream_iterator import CloseableStreamIterator


class AbstractResponseBody(ABC):

    @abstractmethod
    def get_body(self):
        pass


class EmptyResponseBody(AbstractResponseBody):

    def get_body(self):
        return []


class UTF8ResponseBody(AbstractResponseBody):

    def __init__(self, body):
        self._body = body

    def get_body(self):
        return [self._body]


class ByteResponseBody(AbstractResponseBody):
    def __init__(self, body):
        self._body = body

    def get_body(self):
        return [self._body]


class StreamResponseBody(AbstractResponseBody):

    _STREAM_BLOCK_SIZE = 8 * 1024

    def __init__(self, body, reader):
        self._reader = reader
        self._body = body

    def get_body(self):
        return self._reader(self._body, StreamResponseBody._STREAM_BLOCK_SIZE)


class IterableResponseBody(AbstractResponseBody):

    def __init__(self, body):
        self._body = body

    def get_body(self):
        return self._body


class WSGIResponseBodyFactory:

    def __init__(self, reader):
        self._reader = reader

    def create(self, body):
        if body.type == ResponseBodyType.EMPTY:
            return EmptyResponseBody()
        if body.type == ResponseBodyType.UTF8:
            return UTF8ResponseBody(body.content)
        if body.type == ResponseBodyType.BYTE:
            return ByteResponseBody(body.content)
        if body.type == ResponseBodyType.STREAM:
            return StreamResponseBody(body.content, self._reader)
        if body.type == ResponseBodyType.ITERABLE:
            return IterableResponseBody(body.content)
        raise UnknownResponseBodyTypeException("Unknown type for response body: {n}".format(n=body.type.name))


class StreamReaderFactory:

    @staticmethod
    def create_reader(wsgi_file_wrapper):
        if wsgi_file_wrapper is None:
            return CloseableStreamIterator
        return wsgi_file_wrapper


class WSGIResponseAdapter:

    def __init__(self, wsgi_file_wrapper):
        self._wsgi_file_wrapper = wsgi_file_wrapper

    def adapt(self, response):
        headers = [(str(k), str(v)) for k, v in response.headers.items()]
        headers += [CookieHeaderConverter.from_cookie(cookie) for cookie in response.cookies]

        return WSGIResponse(
            response.status.wsgi_format,
            headers,
            WSGIResponseBodyFactory(StreamReaderFactory.create_reader(self._wsgi_file_wrapper)).create(response.body))

