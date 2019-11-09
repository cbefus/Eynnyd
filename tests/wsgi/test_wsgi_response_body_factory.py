from unittest import TestCase

from src.internal.response_body import ResponseBody
from src.internal.response_body_type import ResponseBodyType
from src.internal.wsgi.wsgi_response_body_factory import WSGIResponseBodyFactory
from src.internal.wsgi.empty_response_body import EmptyResponseBody
from src.internal.wsgi.utf8_response_body import UTF8ResponseBody
from src.internal.wsgi.stream_response_body import StreamResponseBody
from src.internal.wsgi.byte_response_body import ByteResponseBody
from src.internal.wsgi.iterable_response_body import IterableResponseBody
from src.exceptions import UnknownResponseBodyTypeException


class TestWSGIResponseBodyFactory(TestCase):

    def test_build_empty(self):
        body = ResponseBody(ResponseBodyType.EMPTY, "who cares")
        self.assertTrue(isinstance(WSGIResponseBodyFactory(None).create(body), EmptyResponseBody))

    def test_build_utf8(self):
        body = ResponseBody(ResponseBodyType.UTF8, "who cares")
        self.assertTrue(isinstance(WSGIResponseBodyFactory(None).create(body), UTF8ResponseBody))

    def test_build_stream(self):
        body = ResponseBody(ResponseBodyType.STREAM, "who cares")
        self.assertTrue(isinstance(WSGIResponseBodyFactory(None).create(body), StreamResponseBody))

    def test_build_byte(self):
        body = ResponseBody(ResponseBodyType.BYTE, "who cares")
        self.assertTrue(isinstance(WSGIResponseBodyFactory(None).create(body), ByteResponseBody))

    def test_build_iterable(self):
        body = ResponseBody(ResponseBodyType.ITERABLE, "who cares")
        self.assertTrue(isinstance(WSGIResponseBodyFactory(None).create(body), IterableResponseBody))

    def test_build_unknown_raises(self):
        class FakeType:
            def name(self):
                return "unknown"
        body = ResponseBody(FakeType(), "who cares")
        with self.assertRaises(UnknownResponseBodyTypeException):
            WSGIResponseBodyFactory(None).create(body)









