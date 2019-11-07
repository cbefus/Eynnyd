import inspect
import logging
from http import HTTPStatus

from src.exceptions import ExceptionHandlingRegisterException, NoGenericExceptionHandlerRegistered, \
    RouteNotFoundException, CallbackIncorrectNumberOfParametersException, NonCallableExceptionHandlerException, \
    InvalidCookieHeaderException
from src.response import ResponseBuilder

LOG = logging.getLogger("exception_handlers")


class ExceptionHandlers:

    def __init__(
            self,
            pre_response_error_handlers,
            post_response_error_handlers):
        self._pre_response_error_handlers = pre_response_error_handlers
        self._post_response_error_handlers = post_response_error_handlers

    def handle_pre_response_error(self, exc, request):
        return ExceptionHandlers._get_handler_for_exception(exc, self._pre_response_error_handlers)(exc, request)

    def handle_post_response_error(self, exc, request, response):
        return ExceptionHandlers\
            ._get_handler_for_exception(exc, self._post_response_error_handlers)(exc, request, response)

    @staticmethod
    def _get_handler_for_exception(exc, error_handlers):
        for k, v in error_handlers:
            if isinstance(exc, k):
                return v
        raise NoGenericExceptionHandlerRegistered("No exception handler registered for even generic exceptions.", exc)




