from eynnyd.internal.wsgi.abstract_response_body import AbstractResponseBody


class StreamResponseBody(AbstractResponseBody):

    _STREAM_BLOCK_SIZE = 8 * 1024

    def __init__(self, body, reader):
        self._reader = reader
        self._body = body

    def get_body(self):
        return self._reader(self._body, StreamResponseBody._STREAM_BLOCK_SIZE)