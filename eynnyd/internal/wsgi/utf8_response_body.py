from eynnyd.internal.wsgi.abstract_response_body import AbstractResponseBody


class UTF8ResponseBody(AbstractResponseBody):

    def __init__(self, body):
        self._body = body

    def get_body(self):
        return [self._body]