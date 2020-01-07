from unittest import TestCase

from eynnyd.internal.wsgi.closeable_stream_iterator import CloseableStreamIterator


class TestCloseableStreamIterator(TestCase):

    def test_spy_streamable_body(self):
        class SpyStreamableBody:
            def __init__(self, size=500):
                self._size = size
                self._read_call_count = 0
                self._close_called = False

            @property
            def read_call_count(self):
                return self._read_call_count

            @property
            def close_called(self):
                return self._close_called

            def read(self, block_size):
                self._size -= block_size
                self._read_call_count += 1
                if self._size < 0:
                    return b""
                else:
                    return b"some content"

            def close(self):
                self._close_called = True

        body = SpyStreamableBody()
        stream = CloseableStreamIterator(body, 100)
        for _ in stream:
            pass
        stream.close()
        self.assertEqual(6, body.read_call_count)
        self.assertTrue(body.close_called)

    def test_spy_streamable_body_no_close(self):
        class SpyStreamableBody:
            def __init__(self, size=500):
                self._size = size
                self._read_call_count = 0

            @property
            def read_call_count(self):
                return self._read_call_count

            def read(self, block_size):
                self._size -= block_size
                self._read_call_count += 1
                if self._size < 0:
                    return b""
                else:
                    return b"some content"

        body = SpyStreamableBody()
        stream = CloseableStreamIterator(body, 100)
        for _ in stream:
            pass
        stream.close()
        self.assertEqual(6, body.read_call_count)