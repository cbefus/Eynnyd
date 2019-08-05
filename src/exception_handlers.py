import logging
from http import HTTPStatus
from optional import Optional

from src.routing.route_tree_traverser import RouteNotFoundException
from src.response import ResponseBuilder

LOG = logging.getLogger("exception_handlers")


class ExceptionHandlers:

    def __init__(self, handlers_by_exception):
        self._handlers_by_exception = handlers_by_exception

    def handle_request_parsing(self, exc, request):
        return self._get_handler_for_exception(exc)(exc, Optional.of(request), Optional.empty())

    def handle_route_finding(self, exc, request):
        return self._get_handler_for_exception(exc)(exc, Optional.of(request), Optional.empty())

    def handle_plan_execution(self, exc, request):
        return self._get_handler_for_exception(exc)(exc, Optional.of(request), Optional.empty())

    def handle_response_adaption(self, exc, response):
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
        if self._is_registered_already(exc):
            raise ExceptionHandlingRegisterException(
                "Cannot register exc: {e} to more than one handler.".format(e=str(exc)))
        self._handlers_by_exception.append((exc, handler))
        return self

    def create(self):
        if not self._is_registered_already(RouteNotFoundException):
            self.register(RouteNotFoundException, default_route_not_found_exception_handler)

        # TODO: Any other defaults?

        if not self._is_registered_already(Exception):
            self.register(Exception, default_internal_server_error_exception_handler)

        return ExceptionHandlers(self._handlers_by_exception)

    def _is_registered_already(self, exc):
        for k, _ in self._handlers_by_exception:
            if k == exc:
                return True
        return False


class ExceptionHandlingRegisterException(Exception):
    pass


class NoGenericExceptionHandlerRegistered(Exception):
    pass


