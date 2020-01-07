import inspect
import logging


from eynnyd.internal.plan_execution.error_handlers import ErrorHandlers
from eynnyd.internal.plan_execution.default_error_handlers import default_route_not_found_error_handler, \
    default_internal_server_error_error_handler, default_internal_server_error_error_handler_only_request, \
    default_invalid_cookie_header_error_handler
from eynnyd.exceptions import ErrorHandlingBuilderException, RouteNotFoundException, \
    CallbackIncorrectNumberOfParametersException, NonCallableExceptionHandlerException, \
    InvalidCookieHeaderException


LOG = logging.getLogger("error_handlers_builder")


class ErrorHandlersBuilder:
    """
    An object for setting handlers for any exceptions that can come up.

    There are two times an error can be thrown in the process of turning a request into a response.  Either the
    error occurs before we have a response or after.  Handlers should be set based on where the exception
    is expected (or in both places if it can come up anywhere).

    Handling will prefer the most specific exception but will execute against a base exception if one was set.

    Several default handlers are set if they are not set manually.  The defaults registered
    are for RouteNotFound, InvalidCookieHeader, and Exception.
    """

    def __init__(self):
        self._pre_response_error_handlers = []
        self._post_response_error_handler = []

    def add_pre_response_error_handler(self, error_class, handler):
        """
        Add error handlers which happen before we have built a response (returned from a handler).

        :param error_class: The class to execute the handler for.
        :param handler: A function which takes a request as a parameter.
        :return: This builder so that fluent design can optionally be used.
        """
        if not hasattr(handler, '__call__'):
            raise NonCallableExceptionHandlerException(
                "Pre Response Error Handler for error {e} is not callable.".format(e=str(error_class)))
        if 2 != len(inspect.signature(handler).parameters):
            raise CallbackIncorrectNumberOfParametersException(
                "Pre Response Error Handler for error {e} does not take exactly 2 argument "
                "(the error, the request)".format(e=str(error_class)))

        if ErrorHandlersBuilder._is_registered_already(error_class, self._pre_response_error_handlers):
            raise ErrorHandlingBuilderException(
                "Cannot associate error: {e} to more than one handler for pre response errors."
                    .format(e=str(error_class)))
        self._pre_response_error_handlers.append((error_class, handler))
        return self

    def add_post_response_error_handler(self, error_class, handler):
        """
        Add error handlers which happen after we have built a response.

        :param error_class: The class to execute the handler for.
        :param handler: A function which takes both a request and response parameter.
        :return:  This builder so that fluent design can optionally be used.
        """
        if not hasattr(handler, '__call__'):
            raise NonCallableExceptionHandlerException(
                "Post Response Error Handler for exception {e} is not callable.".format(e=str(error_class)))
        if 3 != len(inspect.signature(handler).parameters):
            raise CallbackIncorrectNumberOfParametersException(
                "Post Response Error Handler for error {e} does not take exactly 3 argument "
                "(the error, the request, the response)".format(e=str(error_class)))

        if ErrorHandlersBuilder._is_registered_already(error_class, self._post_response_error_handler):
            raise ErrorHandlingBuilderException(
                "Cannot associate error: {e} to more than one handler for post response errors."
                    .format(e=str(error_class)))
        self._post_response_error_handler.append((error_class, handler))
        return self

    def build(self):
        """
       set defaults and build the error handlers for setting into the Eynnyd WebAppBuilder.

        :return: The ErrorHandlers required by the Eynnyd WebAppBuilder set_error_handlers method.
        """
        if not ErrorHandlersBuilder._is_registered_already(
                RouteNotFoundException,
                self._pre_response_error_handlers):
            self.add_pre_response_error_handler(
                RouteNotFoundException,
                default_route_not_found_error_handler)

        if not ErrorHandlersBuilder._is_registered_already(
                InvalidCookieHeaderException,
                self._pre_response_error_handlers):
            self.add_pre_response_error_handler(
                InvalidCookieHeaderException,
                default_invalid_cookie_header_error_handler)

        if not ErrorHandlersBuilder._is_registered_already(
                Exception,
                self._pre_response_error_handlers):
            self.add_pre_response_error_handler(
                Exception,
                default_internal_server_error_error_handler_only_request)

        if not ErrorHandlersBuilder._is_registered_already(
                Exception,
                self._post_response_error_handler):
            self.add_post_response_error_handler(
                Exception,
                default_internal_server_error_error_handler)

        return ErrorHandlers(
            self._pre_response_error_handlers,
            self._post_response_error_handler)

    @staticmethod
    def _is_registered_already(exc, error_handlers):
        for k, _ in error_handlers:
            if k == exc:
                return True
        return False