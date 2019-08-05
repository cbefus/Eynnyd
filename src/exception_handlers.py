from optional import Optional

from src.routing.route_tree_traverser import RouteNotFoundException


class ExceptionHandlers:

    def __init__(self, handlers_by_exception):
        self._handlers_by_exception = handlers_by_exception

    def handle_request_parsing(self, exc, request):
        return self._get_handler_for_exception(exc)(Optional.of(request), Optional.empty())

    def handle_route_finding(self, exc, request):
        return self._get_handler_for_exception(exc)(Optional.of(request), Optional.empty())

    def handle_plan_execution(self, exc, request):
        return self._get_handler_for_exception(exc)(Optional.of(request), Optional.empty())

    def handle_response_adaption(self, exc, response):
        return self._get_handler_for_exception(exc)(Optional.empty(), Optional.of(response))

    def _get_handler_for_exception(self, exc):
        for k, v in self._handlers_by_exception:
            if isinstance(exc(), k):
                return v
        # TODO: What if we don't find the exception -- shouldnt be possible if we register a base exception handler...


class ExceptionHandlersRegistry:

    def __init__(self):
        self._handlers_by_exception = []

    def register(self, exc, handler):
        if self._is_registered_already(exc):
            raise ExceptionHandlingRegisterException(
                "Cannot register exc: {e} to more than one handler.".format(e=str(exc)))
        self._handlers_by_exception.append((exc, handler))

    def create(self):
        if not self._is_registered_already(RouteNotFoundException):
            # TODO Add a default catch all
            pass

        # TODO: Any other defaults?

        if not self._is_registered_already(Exception):
            # TODO Add a default 404
            pass

        return ExceptionHandlers(self._handlers_by_exception)

    def _is_registered_already(self, exc):
        for k, _ in self._handlers_by_exception:
            if k == exc:
                return True
        return False


class ExceptionHandlingRegisterException(Exception):
    pass
