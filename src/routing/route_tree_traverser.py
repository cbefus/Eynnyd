
from src.utils.uri_components_converter import URIComponentsConverter
from src.routing.route_tree import HandlerNotFoundException
from src.plan_execution.execution_plan import ExecutionPlanBuilder


class RouteTreeTraverser:

    @staticmethod
    def traverse(route_tree_root, http_method, uri_path):
        try:
            return route_tree_root.create_execution_plan(
                ExecutionPlanBuilder(),
                [""] + URIComponentsConverter.from_uri(uri_path),  # add an element for the root node.
                http_method)
        except HandlerNotFoundException as e:
            raise RouteNotFoundException(
                "No route found for path {p} and method {m}".format(p=uri_path, m=http_method),
                e)


class RouteNotFoundException(Exception):
    pass

