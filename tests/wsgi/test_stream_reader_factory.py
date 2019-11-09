from unittest import TestCase

from src.internal.wsgi.stream_reader_factory import StreamReaderFactory
from src.internal.wsgi.closeable_stream_iterator import CloseableStreamIterator


class TestStreamReaderFactory(TestCase):

    def test_create_reader_from_passed_in(self):
        self.assertEqual("foobar", StreamReaderFactory.create_reader("foobar"))

    def test_create_reader_from_none(self):
        self.assertEqual(CloseableStreamIterator, StreamReaderFactory.create_reader(None))

