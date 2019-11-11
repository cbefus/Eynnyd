import inspect
import logging


from src.internal.plan_execution.exception_handlers import ExceptionHandlers
from src.internal.plan_execution.default_exception_handlers import default_route_not_found_exception_handler, \
    default_internal_server_error_exception_handler, default_internal_server_error_exception_handler_only_request, \
    default_invalid_cookie_header_exception_handler
from src.exceptions import ExceptionHandlingRegisterException, RouteNotFoundException, \
    CallbackIncorrectNumberOfParametersException, NonCallableExceptionHandlerException, \
    InvalidCookieHeaderException


LOG = logging.getLogger("exception_handlers_registry")


class ExceptionHandlersRegistry:
    """
    An object for registering handlers for any exceptions that can come up.

    There are two times an error can be thrown in the process of turning a request into a response.  Either the
    error occurs before we have a response or after.  Handlers should be registered based on where the exception
    is expected (or in both places if it can come up anywhere).

    Handling will prefer the most specific exception but will execute against a base exception if one was registered.

    Several default handlers are registered if they are not registered against first.  The defaults registered
    are for RouteNotFound, InvalidCookieHeader, and Exception.
    """

    def __init__(self):
        self._pre_response_error_handlers = []
        self._post_response_error_handler = []

    def register_pre_response_error_handler(self, exception_class, handler):
        """
        Registering error handlers which happen before we have built a response (returned from a handler).

        :param exception_class: The class to execute the handler for.
        :param handler: A function which takes a request as a parameter.
        :return: This builder so that fluent design can optionally be used.
        """
        if not hasattr(handler, '__call__'):
            raise NonCallableExceptionHandlerException(
                "Pre Response Error Handler for exception {e} is not callable.".format(e=str(exception_class)))
        if 2 != len(inspect.signature(handler).parameters):
            raise CallbackIncorrectNumberOfParametersException(
                "Pre Response Error Handler for exception {e} does not take exactly 2 argument "
                "(the exception, the request)".format(e=str(exception_class)))

        if ExceptionHandlersRegistry._is_registered_already(exception_class, self._pre_response_error_handlers):
            raise ExceptionHandlingRegisterException(
                "Cannot register exc: {e} to more than one handler for pre response exceptions."
                    .format(e=str(exception_class)))
        self._pre_response_error_handlers.append((exception_class, handler))
        return self

    def register_post_response_error_handler(self, exception_class, handler):
        """
        Registering error handlers which happen after we have built a response.

        :param exception_class: The class to execute the handler for.
        :param handler: A function which takes both a request and response parameter.
        :return:  This builder so that fluent design can optionally be used.
        """
        if not hasattr(handler, '__call__'):
            raise NonCallableExceptionHandlerException(
                "Post Response Exception Handler for exception {e} is not callable.".format(e=str(exception_class)))
        if 3 != len(inspect.signature(handler).parameters):
            raise CallbackIncorrectNumberOfParametersException(
                "Post Response  Exception Handler for exception {e} does not take exactly 3 argument "
                "(the exception, the request, the response)".format(e=str(exception_class)))

        if ExceptionHandlersRegistry._is_registered_already(exception_class, self._post_response_error_handler):
            raise ExceptionHandlingRegisterException(
                "Cannot register exc: {e} to more than one handler for post response exceptions."
                    .format(e=str(exception_class)))
        self._post_response_error_handler.append((exception_class, handler))
        return self

    def create(self):
        """
        Create the error handlers for setting into the Eynnyd WebAppBuilder.

        :return: The ExceptionHandlers required by the Eynnyd WebAppBuilder set_error_handlers method.
        """
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