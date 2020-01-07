from eynnyd.internal.wsgi.abstract_response_body import AbstractResponseBody


class EmptyResponseBody(AbstractResponseBody):

    def get_body(self):
        return []
