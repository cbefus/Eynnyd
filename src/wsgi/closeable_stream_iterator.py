
class CloseableStreamIterator:

    def __init__(self, stream, block_size):
        self._stream = stream
        self._block_size = block_size

    def __iter__(self):
        return self

    def __next__(self):
        data = self._stream.read(self._block_size)

        if data == b'':
            raise StopIteration
        return data

    def close(self):
        try:
            self._stream.close()
        except (AttributeError, TypeError):
            pass
