

class PlanExecutor:

    @staticmethod
    def execute(execution_plan, request):
        new_request = \
            PlanExecutor._update_request_via_request_interceptors(execution_plan.request_interceptors, request)
        response = \
            PlanExecutor._get_response_from_handler(execution_plan.handler, new_request)
        return PlanExecutor\
            ._update_response_via_response_interceptors(execution_plan.response_interceptors, response, new_request)

    @staticmethod
    def _update_request_via_request_interceptors(request_interceptors, request):
        new_request = request
        for request_interceptor in request_interceptors:
            new_request = request_interceptor(new_request)
            #  TODO: We should validate that this new request is still a request right?
        return new_request

    @staticmethod
    def _get_response_from_handler(handler, request):
        response = handler(request)
        # TODO: We should validate that this response is a response right?
        return response

    @staticmethod
    def _update_response_via_response_interceptors(response_interceptors, response, request):
        new_response = response
        for response_interceptor in reversed(response_interceptors):
            new_response = response_interceptor(request, new_response)
            # TODO: We should validate that this response is still a response right?
        return new_response
