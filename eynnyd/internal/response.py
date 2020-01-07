from eynnyd.abstract_response import AbstractResponse


class Response(AbstractResponse):

    def __init__(self, status, body, headers, cookies):
        self._status = status
        self._body = body
        self._headers = headers
        self._cookies = cookies

    @property
    def status(self):
        return self._status

    @property
    def body(self):
        return self._body

    @property
    def headers(self):
        return self._headers

    @property
    def cookies(self):
        return self._cookies

    def __str__(self):
        return "<{c}>".format(c=self.status)
