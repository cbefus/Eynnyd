
from eynnyd.internal.utils.uri_components_converter import URIComponentsConverter
from eynnyd.exceptions import HandlerNotFoundException, RouteNotFoundException
from eynnyd.internal.plan_execution.execution_plan_builder import ExecutionPlanBuilder


class RouteTreeTraverser:

    @staticmethod
    def traverse(route_tree_root, http_method, uri_path):
        try:
            return route_tree_root.create_execution_plan(
                ExecutionPlanBuilder(),
                URIComponentsConverter.from_uri(uri_path),
                http_method)
        except HandlerNotFoundException as e:
            raise RouteNotFoundException(
                "No route found for path {p} and method {m}".format(p=uri_path, m=http_method),
                e)

