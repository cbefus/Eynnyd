from optional import Optional

from eynnyd.internal.plan_execution.execution_plan import ExecutionPlan
from eynnyd.exceptions import ExecutionPlanBuildException


class ExecutionPlanBuilder:

    def __init__(self):
        self._request_interceptors = []
        self._handler = Optional.empty()
        self._response_interceptors = []
        self._path_parameters = {}

    def add_request_interceptors(self, request_interceptors):
        self._request_interceptors.extend(request_interceptors)
        return self

    def add_response_interceptors(self, response_interceptors):
        self._response_interceptors.extend(response_interceptors)
        return self

    def set_handler(self, handler):
        self._handler = Optional.of(handler)
        return self

    def add_path_parameter(self, name_from_route, value_from_request):
        self._path_parameters[name_from_route] = value_from_request
        return self

    def build(self):
        return ExecutionPlan(
            self._request_interceptors,
            self._handler.get_or_raise(
                ExecutionPlanBuildException("Cannot build an execution plan without a handler.")),
            self._response_interceptors,
            self._path_parameters)


