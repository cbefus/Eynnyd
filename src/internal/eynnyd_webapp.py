import logging

from src.internal.wsgi_loaded_request import WSGILoadedRequest
from src.internal.routing.route_tree_traverser import RouteTreeTraverser
from src.internal.plan_execution.plan_executor import PlanExecutor
from src.internal.wsgi.raw_wsgi_server_error_response import RawWSGIServerErrorResponse
from src.internal.wsgi.wsgi_response_adapter import WSGIResponseAdapter

LOG = logging.getLogger("eynnyd_webapp")


class EynnydWebapp:

    def __init__(self, route_tree, exception_handlers):
        self._route_tree = route_tree
        self._exception_handlers = exception_handlers
        self._plan_executor = PlanExecutor(self._exception_handlers)

    def __call__(self, wsgi_environment, wsgi_start_response):  # pragma: no cover
        try:
            wsgi_response = self._wsgi_input_to_wsgi_output(wsgi_environment)
        except Exception as e:
            LOG.exception("Unexpected error thrown, wsgi environment was: {wsgi}".format(wsgi=wsgi_environment))
            wsgi_response = RawWSGIServerErrorResponse()

        wsgi_start_response(wsgi_response.status, wsgi_response.headers)
        return wsgi_response.body

    def _wsgi_input_to_wsgi_output(self, wsgi_environment):  # pragma: no cover
        wsgi_loaded_request = WSGILoadedRequest(wsgi_environment)
        response = self.process_request_to_response(wsgi_loaded_request)
        try:
            return WSGIResponseAdapter(wsgi_environment.get("wsgi.file_wrapper")).adapt(response)
        except Exception as e:
            error_response = self._exception_handlers.handle_post_response_error(e, wsgi_loaded_request, response)
            return WSGIResponseAdapter(wsgi_environment.get("wsgi.file_wrapper")).adapt(error_response)

    def process_request_to_response(self, wsgi_loaded_request):
        try:
            execution_plan = \
                RouteTreeTraverser.traverse(
                    self._route_tree,
                    wsgi_loaded_request.http_method,
                    wsgi_loaded_request.request_uri.path)
        except Exception as e:
            return self._exception_handlers.handle_pre_response_error(e, wsgi_loaded_request)

        updated_request = wsgi_loaded_request.copy_and_set_path_parameters(execution_plan.path_parameters)
        return self._plan_executor.execute_plan(execution_plan, updated_request)


