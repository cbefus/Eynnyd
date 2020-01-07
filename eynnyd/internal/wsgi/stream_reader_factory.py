from eynnyd.internal.wsgi.closeable_stream_iterator import CloseableStreamIterator


class StreamReaderFactory:

    @staticmethod
    def create_reader(wsgi_file_wrapper):
        if wsgi_file_wrapper is None:
            return CloseableStreamIterator
        return wsgi_file_wrapper