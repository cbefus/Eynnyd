import inspect
import logging


from src.plan_execution.exception_handlers import ExceptionHandlers
from src.plan_execution.default_exception_handlers import default_route_not_found_exception_handler, \
    default_internal_server_error_exception_handler, default_internal_server_error_exception_handler_only_request, \
    default_invalid_cookie_header_exception_handler
from src.exceptions import ExceptionHandlingRegisterException, RouteNotFoundException, \
    CallbackIncorrectNumberOfParametersException, NonCallableExceptionHandlerException, \
    InvalidCookieHeaderException


LOG = logging.getLogger("exception_handlers_registry")


class ExceptionHandlersRegistry:

    def __init__(self):
        self._pre_response_error_handlers = []
        self._post_response_error_handler = []

    def register_pre_response_error_handler(self, exc, handler):
        if not hasattr(handler, '__call__'):
            raise NonCallableExceptionHandlerException(
                "Pre Response Error Handler for exception {e} is not callable.".format(e=str(exc)))
        if 2 != len(inspect.signature(handler).parameters):
            raise CallbackIncorrectNumberOfParametersException(
                "Pre Response Error Handler for exception {e} does not take exactly 2 argument "
                "(the exception, the request)".format(e=str(exc)))

        if ExceptionHandlersRegistry._is_registered_already(exc, self._pre_response_error_handlers):
            raise ExceptionHandlingRegisterException(
                "Cannot register exc: {e} to more than one handler for pre response exceptions.".format(e=str(exc)))
        self._pre_response_error_handlers.append((exc, handler))
        return self

    def register_post_response_error_handler(self, exc, handler):
        if not hasattr(handler, '__call__'):
            raise NonCallableExceptionHandlerException(
                "Post Response Exception Handler for exception {e} is not callable.".format(e=str(exc)))
        if 3 != len(inspect.signature(handler).parameters):
            raise CallbackIncorrectNumberOfParametersException(
                "Post Response  Exception Handler for exception {e} does not take exactly 3 argument "
                "(the exception, the request, the response)".format(e=str(exc)))

        if ExceptionHandlersRegistry._is_registered_already(exc, self._post_response_error_handler):
            raise ExceptionHandlingRegisterException(
                "Cannot register exc: {e} to more than one handler for post response exceptions."
                    .format(e=str(exc)))
        self._post_response_error_handler.append((exc, handler))
        return self

    def create(self):
        if not ExceptionHandlersRegistry._is_registered_already(
                RouteNotFoundException,
                self._pre_response_error_handlers):
            self.register_pre_response_error_handler(
                RouteNotFoundException,
                default_route_not_found_exception_handler)

        if not ExceptionHandlersRegistry._is_registered_already(
                InvalidCookieHeaderException,
                self._pre_response_error_handlers):
            self.register_pre_response_error_handler(
                InvalidCookieHeaderException,
                default_invalid_cookie_header_exception_handler)

        if not ExceptionHandlersRegistry._is_registered_already(
                Exception,
                self._pre_response_error_handlers):
            self.register_pre_response_error_handler(
                Exception,
                default_internal_server_error_exception_handler_only_request)

        if not ExceptionHandlersRegistry._is_registered_already(
                Exception,
                self._post_response_error_handler):
            self.register_post_response_error_handler(
                Exception,
                default_internal_server_error_exception_handler)

        return ExceptionHandlers(
            self._pre_response_error_handlers,
            self._post_response_error_handler)

    @staticmethod
    def _is_registered_already(exc, exception_handlers):
        for k, _ in exception_handlers:
            if k == exc:
                return True
        return False