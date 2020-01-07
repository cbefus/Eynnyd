from eynnyd.internal.response_body_type import ResponseBodyType


class ResponseBody:

    def __init__(self, type, content):
        self._type = type
        self._content = content

    @staticmethod
    def empty_response():
        return ResponseBody(ResponseBodyType.EMPTY, "")

    @property
    def type(self):
        return self._type

    @property
    def content(self):
        return self._content