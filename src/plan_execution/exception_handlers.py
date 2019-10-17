import inspect
import logging
from http import HTTPStatus
from optional import Optional

from src.exceptions import ExceptionHandlingRegisterException, NoGenericExceptionHandlerRegistered, \
    RouteNotFoundException, CallbackIncorrectNumberOfParametersException, NonCallableExceptionHandlerException, \
    InvalidCookieHeaderException
from src.response import ResponseBuilder

LOG = logging.getLogger("exception_handlers")


class ExceptionHandlers:

    def __init__(self, handlers_by_exception):
        self._handlers_by_exception = handlers_by_exception

    def handle_while_having_a_request(self, exc, request):
        return self._get_handler_for_exception(exc)(exc, Optional.of(request), Optional.empty())

    def handle_while_having_a_request_and_response(self, exc, request, response):
        return self._get_handler_for_exception(exc)(exc, Optional.of(request), Optional.of(response))

    def handle_while_having_a_response(self, exc, response):
        return self._get_handler_for_exception(exc)(exc, Optional.empty(), Optional.of(response))

    def _get_handler_for_exception(self, exc):
        for k, v in self._handlers_by_exception:
            if isinstance(exc, k):
                return v
        raise NoGenericExceptionHandlerRegistered("No exception handler registered for even generic exceptions.", exc)


def default_route_not_found_exception_handler(exc, request, response):
    body = "No Route Found."
    if request.is_present():
        body = \
            "No Route Found for Http Method '{m}' on path '{p}'."\
                .format(m=request.get().http_method, p=request.get().request_uri)

    return ResponseBuilder()\
        .set_status(HTTPStatus.NOT_FOUND)\
        .set_body(body)\
        .build()


def default_invalid_cookie_header_exception_handler(exc, request, response):
    LOG.warning(
        "Request attempted with invalid cookie header: {rc}".format(rc=str(request.get().headers.get("COOKIE"))))
    return ResponseBuilder()\
        .set_status(HTTPStatus.BAD_REQUEST)\
        .set_body(
            "Invalid cookies sent (Did you forget to URLEncode them?). "
            "Check your formatting against RFC6265 standards.")\
        .build()


def default_internal_server_error_exception_handler(exc, request, response):
    LOG.exception("Unexpected exception occured.", exc_info=exc)
    return ResponseBuilder()\
        .set_status(HTTPStatus.INTERNAL_SERVER_ERROR)\
        .set_body("Internal Server Error")\
        .build()


class ExceptionHandlersRegistry:

    def __init__(self):
        self._handlers_by_exception = []

    def register(self, exc, handler):
        if not hasattr(handler, '__call__'):
            raise NonCallableExceptionHandlerException(
                "Exception Handler for exception {e} is not callable.".format(e=str(exc)))
        if 3 != len(inspect.signature(handler).parameters):
            raise CallbackIncorrectNumberOfParametersException(
                "Exception Handler for exception {e} does not take exactly 3 argument "
                "(the exception, optional request, optional response)".format(e=str(exc)))

        if self._is_registered_already(exc):
            raise ExceptionHandlingRegisterException(
                "Cannot register exc: {e} to more than one handler.".format(e=str(exc)))
        self._handlers_by_exception.append((exc, handler))
        return self

    def create(self):
        if not self._is_registered_already(RouteNotFoundException):
            self.register(RouteNotFoundException, default_route_not_found_exception_handler)

        if not self._is_registered_already(InvalidCookieHeaderException):
            self.register(InvalidCookieHeaderException, default_invalid_cookie_header_exception_handler)

        if not self._is_registered_already(Exception):
            self.register(Exception, default_internal_server_error_exception_handler)

        return ExceptionHandlers(self._handlers_by_exception)

    def _is_registered_already(self, exc):
        for k, _ in self._handlers_by_exception:
            if k == exc:
                return True
        return False
