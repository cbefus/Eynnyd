from optional import Optional
import logging

from src.exceptions import EynnydWebappBuildException
from src.request import WSGILoadedRequest
from src.routing.route_tree_traverser import RouteTreeTraverser
from src.plan_execution.plan_executor import PlanExecutor
from src.wsgi.wsgi_response import RawWSGIServerError
from src.wsgi.wsgi_response_adapter import WSGIResponseAdapter
from src.plan_execution.exception_handlers import ExceptionHandlersRegistry

LOG = logging.getLogger("eynnyd_webapp")


class EynnydWebapp:

    def __init__(self, route_tree, exception_handlers):
        self._route_tree = route_tree
        self._exception_handlers = exception_handlers

    def __call__(self, wsgi_environment, wsgi_start_response):
        try:
            wsgi_response = self._wsgi_input_to_wsgi_output(wsgi_environment)
        except Exception as e:
            LOG.exception("Unexpected error thrown")
            wsgi_response = RawWSGIServerError()

        wsgi_start_response(wsgi_response.status, wsgi_response.headers)
        return wsgi_response.body

    def _wsgi_input_to_wsgi_output(self, wsgi_environment):
        try:
            request = WSGILoadedRequest(wsgi_environment)
        except Exception as e:
            return self._exception_handlers.handle_while_having_a_request(e, wsgi_environment)  # fix this, its a lie

        response = self.process_request_to_response(request)
        try:
            return WSGIResponseAdapter.adapt(response)
        except Exception as e:
            error_response = self._exception_handlers.handle_while_having_a_response(e, response)
            return WSGIResponseAdapter.adapt(error_response)

    def process_request_to_response(self, request):
        try:
            execution_plan = \
                RouteTreeTraverser.traverse(
                    self._route_tree,
                    request.http_method,
                    request.request_uri.path)
        except Exception as e:
            return self._exception_handlers.handle_while_having_a_request(e, request)

        updated_request = request.copy_and_set_path_parameters(execution_plan.path_parameters)

        try:
            intercepted_request = PlanExecutor.execute_request_interceptors(execution_plan, updated_request)
        except Exception as e:
            return self._exception_handlers.handle_while_having_a_request(e, updated_request)

        try:
            handler_response = PlanExecutor.execute_handler(execution_plan, intercepted_request)
        except Exception as e:
            return self._exception_handlers.handle_while_having_a_request(e, intercepted_request)

        try:
            return PlanExecutor.execute_response_interceptors(execution_plan, intercepted_request, handler_response)
        except Exception as e:
            return self._exception_handlers\
                .handle_while_having_a_request_and_response(e, intercepted_request, handler_response)


class EynnydWebappBuilder:

    def __init__(self):
        self._routes = Optional.empty()
        self._exception_handlers = ExceptionHandlersRegistry().create()

    def set_routes(self, root_tree_node):
        self._routes = Optional.of(root_tree_node)
        return self

    def set_error_handlers(self, exception_handlers):
        self._exception_handlers = exception_handlers
        return self

    def build(self):
        return EynnydWebapp(
            self._routes.get_or_raise(EynnydWebappBuildException(
                "You must set routes for the webapp to route requests too.")),
            self._exception_handlers)
