from eynnyd.exceptions import UnknownResponseBodyTypeException
from eynnyd.internal.response_body_type import ResponseBodyType
from eynnyd.internal.wsgi.byte_response_body import ByteResponseBody
from eynnyd.internal.wsgi.empty_response_body import EmptyResponseBody
from eynnyd.internal.wsgi.iterable_response_body import IterableResponseBody
from eynnyd.internal.wsgi.stream_response_body import StreamResponseBody
from eynnyd.internal.wsgi.utf8_response_body import UTF8ResponseBody


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