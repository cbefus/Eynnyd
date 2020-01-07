from unittest import TestCase

from eynnyd.internal.wsgi.stream_response_body import StreamResponseBody


class TestStreamResponseBody(TestCase):

    def test_get_body(self):
        class FakeReader:
            def __init__(self, body, block_size):
                self._body = body
                self._block_size = block_size

            def __iter__(self):
                return self

            def __next__(self):
                if self._block_size > 0:
                    self._block_size = 0
                    return self._body
                raise StopIteration

        body = StreamResponseBody("foobar", FakeReader)
        res = []
        for part in body.get_body():
            res.append(part)
        self.assertEqual(["foobar"], res)
