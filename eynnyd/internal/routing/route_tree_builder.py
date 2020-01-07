import logging

from optional import Optional

from eynnyd.exceptions import DuplicateHandlerRoutesException
from eynnyd.internal.routing.pattern_route_builder import PatternRouteBuilder
from eynnyd.internal.routing.route_tree_node import RouteTreeNode

LOG = logging.getLogger("route_tree")


class RouteTeeBuilder:

    def __init__(self):
        self._sub_routes_to_node_builders = {}
        self._request_interceptors = []
        self._http_methods_to_handlers = {}
        self._response_interceptors = []
        self._pattern_route_builder = Optional.empty()

    def add_request_interceptor(self, uri_components, interceptor):
        if len(uri_components) == 0:
            self._request_interceptors.append(interceptor)
            return self

        return self._get_or_build_next_node(uri_components).add_request_interceptor(uri_components[1:], interceptor)

    def add_response_interceptor(self, uri_components, interceptor):
        if len(uri_components) == 0:
            self._response_interceptors.append(interceptor)
            return self

        return self._get_or_build_next_node(uri_components).add_response_interceptor(uri_components[1:], interceptor)

    def add_handler(self, http_method, uri_components, handler):
        if len(uri_components) == 0:
            if http_method in self._http_methods_to_handlers:
                raise DuplicateHandlerRoutesException("Cannot have two handlers with equal routes: {r}".format(r=http_method))
            self._http_methods_to_handlers[http_method] = handler
            return self

        return self._get_or_build_next_node(uri_components).add_handler(http_method, uri_components[1:], handler)

    def build(self):
        return RouteTreeNode(
            self._request_interceptors,
            self._response_interceptors,
            self._http_methods_to_handlers,
            {route: node_builder.build() for route, node_builder in self._sub_routes_to_node_builders.items()},
            self._pattern_route_builder.map(lambda prb: prb.build()))

    def _get_or_build_next_node(self, uri_components):
        next_component = uri_components[0]
        if RouteTeeBuilder._is_pattern_component(next_component):
            if self._pattern_route_builder.is_empty():
                self._pattern_route_builder = Optional.of(PatternRouteBuilder(next_component[1:-1], RouteTeeBuilder()))
            return self._pattern_route_builder.get().pattern_route_node_builder

        if next_component not in self._sub_routes_to_node_builders:
            self._sub_routes_to_node_builders[next_component] = RouteTeeBuilder()
        return self._sub_routes_to_node_builders[next_component]

    @staticmethod
    def _is_pattern_component(uri_component):
        return uri_component.startswith("{") and uri_component.endswith("}")
