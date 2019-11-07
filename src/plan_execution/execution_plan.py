
class ExecutionPlan:

    def __init__(self, request_interceptors, handler, response_interceptors, path_parameters):
        self._request_interceptors = request_interceptors
        self._handler = handler
        self._response_interceptors = response_interceptors
        self._path_parameters = path_parameters

    @property
    def request_interceptors(self):
        return self._request_interceptors

    @property
    def handler(self):
        return self._handler

    @property
    def response_interceptors(self):
        return self._response_interceptors

    @property
    def path_parameters(self):
        return self._path_parameters

