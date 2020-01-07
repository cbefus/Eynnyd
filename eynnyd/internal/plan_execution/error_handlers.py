import logging

from eynnyd.exceptions import NoGenericErrorHandlerException

LOG = logging.getLogger("error_handlers")


class ErrorHandlers:

    def __init__(
            self,
            pre_response_error_handlers,
            post_response_error_handlers):
        self._pre_response_error_handlers = pre_response_error_handlers
        self._post_response_error_handlers = post_response_error_handlers

    def handle_pre_response_error(self, thrown_error, request):
        return ErrorHandlers\
            ._get_handler_for_error(thrown_error, self._pre_response_error_handlers)(thrown_error, request)

    def handle_post_response_error(self, thrown_error, request, response):
        return ErrorHandlers\
            ._get_handler_for_error(
                thrown_error,
                self._post_response_error_handlers)(thrown_error, request, response)

    @staticmethod
    def _get_handler_for_error(thrown_error, error_handlers):
        for registered_error, registered_handler in error_handlers:
            if isinstance(thrown_error, registered_error):
                return registered_handler
        raise NoGenericErrorHandlerException(
            "No error handler registered for even generic exceptions.",
            thrown_error)




