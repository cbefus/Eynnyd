import logging

from src.exceptions import NoGenericExceptionHandlerRegistered

LOG = logging.getLogger("exception_handlers")


class ExceptionHandlers:

    def __init__(
            self,
            pre_response_error_handlers,
            post_response_error_handlers):
        self._pre_response_error_handlers = pre_response_error_handlers
        self._post_response_error_handlers = post_response_error_handlers

    def handle_pre_response_error(self, thrown_exception, request):
        return ExceptionHandlers\
            ._get_handler_for_exception(thrown_exception, self._pre_response_error_handlers)(thrown_exception, request)

    def handle_post_response_error(self, thrown_exception, request, response):
        return ExceptionHandlers\
            ._get_handler_for_exception(
                thrown_exception,
                self._post_response_error_handlers)(thrown_exception, request, response)

    @staticmethod
    def _get_handler_for_exception(thrown_exception, error_handlers):
        for registered_exception, registered_handler in error_handlers:
            if isinstance(thrown_exception, registered_exception):
                return registered_handler
        raise NoGenericExceptionHandlerRegistered(
            "No exception handler registered for even generic exceptions.",
            thrown_exception)




