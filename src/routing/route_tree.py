import logging

from optional import Optional

from src.exceptions import HandlerNotFoundException, DuplicateHandlerRoutesException

LOG = logging.getLogger("route_tree")


class PatternRoute:

    def __init__(self, parameter_name, pattern_route_node):
        self._parameter_name = parameter_name
        self._pattern_route_node = pattern_route_node

    @property
    def parameter_name(self):
        return self._parameter_name

    @property
    def pattern_route_node(self):
        return self._pattern_route_node


class PatternRouteBuilder:

    def __init__(self, parameter_name, pattern_route_node_builder):
        self._parameter_name = parameter_name
        self._pattern_route_node_builder = pattern_route_node_builder

    @property
    def pattern_route_node_builder(self):
        return self._pattern_route_node_builder

    def build(self):
        return PatternRoute(self._parameter_name, self._pattern_route_node_builder.build())


class RouteTreeNode:

    def __init__(
            self,
            request_interceptors,
            response_interceptors,
            http_methods_to_handlers,
            sub_routes_to_nodes,
            pattern_route):
        self._request_interceptors = request_interceptors
        self._response_interceptors = response_interceptors
        self._http_methods_to_handlers = http_methods_to_handlers
        self._sub_routes_to_nodes = sub_routes_to_nodes
        self._pattern_route = pattern_route

    def create_execution_plan(self, execution_plan_builder, uri_components, http_method):
        execution_plan_builder \
            .add_request_interceptors(self._request_interceptors) \
            .add_response_interceptors(self._response_interceptors)

        if len(uri_components) == 0:
            if http_method in self._http_methods_to_handlers:
                return execution_plan_builder.set_handler(self._http_methods_to_handlers.get(http_method)).build()
            raise HandlerNotFoundException("No handler found for method {m}".format(m=http_method))

        if uri_components[0] in self._sub_routes_to_nodes:
            return self._sub_routes_to_nodes.get(uri_components[0])\
                .create_execution_plan(execution_plan_builder, uri_components[1:], http_method)

        if self._pattern_route.is_present():
            execution_plan_builder.add_path_parameter(self._pattern_route.get().parameter_name, uri_components[0])
            return self._pattern_route.get()\
                .pattern_route_node.create_execution_plan(execution_plan_builder, uri_components[1:], http_method)

        raise HandlerNotFoundException("No Route/handler found for method {m} and route".format(m=http_method))


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





