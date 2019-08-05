from optional import Optional
import logging

from src.request import Request
from src.routing.route_tree_traverser import RouteTreeTraverser
from src.plan_executor import PlanExecutor
from src.wsgi_response import RawWSGIServerError
from src.wsgi_response_adapter import WSGIResponseAdapter
from src.exception_handlers import ExceptionHandlersRegistry

LOG = logging.getLogger("eynnyd_webapp")


class EynnydWebapp:

    def __init__(self, route_tree, exception_handlers):
        self._route_tree = route_tree
        self._exception_handlers = exception_handlers

    # TODO: pull the error stream off of the wsgi environment and use it to log errors through to wsgi server
    def __call__(self, wsgi_environment, wsgi_start_response):
        try:
            wsgi_response = self._wsgi_input_to_wsgi_output(wsgi_environment)
        except Exception as e:
            LOG.exception("Unexpected error thrown")
            wsgi_response = RawWSGIServerError()  # TODO: Add context here from environment

        wsgi_start_response(wsgi_response.status, wsgi_response.headers)
        return wsgi_response.body

    def _wsgi_input_to_wsgi_output(self, wsgi_environment):
        response = self._process_to_response(wsgi_environment)
        try:
            return WSGIResponseAdapter.adapt(response)
        except Exception as e:
            error_response = self._exception_handlers.handle_response_adaption(e, response)
            return WSGIResponseAdapter.adapt(error_response)

    def _process_to_response(self, wsgi_environment):
        try:
            request = Request(wsgi_environment)
        except Exception as e:
            return self._exception_handlers.handle_request_parsing(e, wsgi_environment)

        try:
            execution_plan = \
                RouteTreeTraverser.traverse(
                    self._route_tree,
                    request.http_method,
                    request.request_uri.path)
        except Exception as e:
            return self._exception_handlers.handle_route_finding(e, request)

        updated_request = Request.copy_and_set_path_parameters(request, execution_plan.path_parameters)

        try:
            return PlanExecutor.execute(execution_plan, updated_request)
        except Exception as e:
            return self._exception_handlers.handle_plan_execution(e, updated_request)


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


class EynnydWebappBuildException(Exception):
    pass

