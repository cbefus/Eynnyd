from eynnyd.exceptions import RequestInterceptorReturnedNonRequestException, HandlerReturnedNonResponseException, \
    ResponseInterceptorReturnedNonResponseException
from eynnyd.abstract_request import AbstractRequest
from eynnyd.abstract_response import AbstractResponse


class PlanExecutor:

    def __init__(self, error_handlers):
        self._error_handlers = error_handlers

    def execute_plan(self, execution_plan, request):
        try:
            intercepted_request = self._execute_request_interceptors(execution_plan, request)
        except Exception as e:
            return self._error_handlers.handle_pre_response_error(e, request)

        try:
            handler_response = self._execute_handler(execution_plan, intercepted_request)
        except Exception as e:
            return self._error_handlers.handle_pre_response_error(e, intercepted_request)

        try:
            return self._execute_response_interceptors(execution_plan, intercepted_request, handler_response)
        except Exception as e:
            return self._error_handlers\
                .handle_post_response_error(e, intercepted_request, handler_response)


    @staticmethod
    def _execute_request_interceptors(execution_plan, request):
        return PlanExecutor._update_request_via_request_interceptors(execution_plan.request_interceptors, request)

    @staticmethod
    def _execute_handler(execution_plan, request):
        return PlanExecutor._get_response_from_handler(execution_plan.handler, request)

    @staticmethod
    def _execute_response_interceptors(execution_plan, request, response):
        return PlanExecutor\
            ._update_response_via_response_interceptors(execution_plan.response_interceptors, request, response)

    @staticmethod
    def _update_request_via_request_interceptors(request_interceptors, request):
        new_request = request
        for request_interceptor in request_interceptors:
            new_request = request_interceptor(new_request)
            if not isinstance(new_request, AbstractRequest):
                raise RequestInterceptorReturnedNonRequestException(
                    "Request Interceptor {n} did not return a request.".format(n=request_interceptor.__name__))
        return new_request

    @staticmethod
    def _get_response_from_handler(handler, request):
        response = handler(request)
        if not isinstance(response, AbstractResponse):
            raise HandlerReturnedNonResponseException(
                "Request Handler {n} did not return a response.".format(n=handler.__name__))
        return response

    @staticmethod
    def _update_response_via_response_interceptors(response_interceptors, request, response):
        new_response = response
        for response_interceptor in reversed(response_interceptors):
            new_response = response_interceptor(request, new_response)
            if not isinstance(new_response, AbstractResponse):
                raise ResponseInterceptorReturnedNonResponseException(
                    "Response Interceptor {n} did not return a resposne.".format(n=response_interceptor.__name__))
        return new_response

