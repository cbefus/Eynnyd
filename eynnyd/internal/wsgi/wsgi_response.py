
class WSGIResponse:

    def __init__(self, status, headers, body):
        self._status = status
        self._headers = headers
        self._body = body

    @property
    def status(self):
        return self._status

    @property
    def headers(self):
        return self._headers

    @property
    def body(self):
        return self._body


