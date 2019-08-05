import logging

from abc import ABC, abstractmethod
from optional import Optional

LOG = logging.getLogger("route_tree")


class AbstractRouteTreeNode(ABC):

    def __init__(self, sub_routes, request_interceptors, handlers, response_interceptors, pattern_route):
        self._sub_routes = sub_routes
        self._request_interceptors = request_interceptors
        self._handlers = handlers
        self._response_interceptors = response_interceptors
        self._pattern_route = pattern_route

    @abstractmethod
    def create_execution_plan(self, execution_plan_builder, uri_components, http_method):
        pass

    def _get_plan_from_handlers_or_recursing(self, execution_plan_builder, uri_components, http_method):
        if len(uri_components) == 0:
            return self._get_plan_from_handlers_or_raise(execution_plan_builder, http_method)
        return self._get_plan_from_recursing_or_raise(execution_plan_builder, uri_components, http_method)

    def _get_plan_from_handlers_or_raise(self, execution_plan_builder, http_method):
        if http_method in self._handlers:
            return execution_plan_builder \
                .set_handler(self._handlers.get(http_method)) \
                .build()
        raise HandlerNotFoundException("No handler found for method {m} and route".format(m=http_method))

    def _get_plan_from_recursing_or_raise(self, execution_plan_builder, uri_components, http_method):
        if uri_components[0] in self._sub_routes:
            return self._get_plan_from_sub_route(execution_plan_builder, uri_components, http_method)

        if self._pattern_route.is_present():
            return self._get_plan_from_pattern_route(execution_plan_builder, uri_components, http_method)

        raise HandlerNotFoundException("No handler found for method and route")

    def _get_plan_from_sub_route(self, execution_plan_builder, uri_components, http_method):
        return self._sub_routes \
            .get(uri_components[0]) \
            .create_execution_plan(execution_plan_builder, uri_components, http_method)

    def _get_plan_from_pattern_route(self, execution_plan_builder, uri_components, http_method):
        return self._pattern_route \
            .get() \
            .create_execution_plan(execution_plan_builder, uri_components, http_method)


class PatternRouteTreeNode(AbstractRouteTreeNode):

    def __init__(self, parameter_name, sub_routes, request_interceptors, handlers, response_interceptors, pattern_route):
        super().__init__(sub_routes, request_interceptors, handlers, response_interceptors, pattern_route)
        self._parameter_name = parameter_name

    def create_execution_plan(self, execution_plan_builder, uri_components, http_method):
        execution_plan_builder \
            .add_request_interceptors(self._request_interceptors) \
            .add_response_interceptors(self._response_interceptors)\
            .add_path_parameter(self._parameter_name, uri_components[0])

        return self._get_plan_from_handlers_or_recursing(execution_plan_builder, uri_components[1:], http_method)


class RouteTreeNode(AbstractRouteTreeNode):

    def create_execution_plan(self, execution_plan_builder, uri_components, http_method):
        execution_plan_builder\
            .add_request_interceptors(self._request_interceptors)\
            .add_response_interceptors(self._response_interceptors)

        return self._get_plan_from_handlers_or_recursing(execution_plan_builder, uri_components[1:], http_method)


class BaseRouteTeeNodeBuilder(ABC):

    def __init__(self):
        self._sub_routes_builders = {}
        self._request_interceptors = []
        self._handlers = {}
        self._response_interceptors = []
        self._pattern_route_builder = Optional.empty()

    @abstractmethod
    def build(self):
        pass

    def add_request_interceptor(self, uri_components, interceptor):
        if len(uri_components) == 0:
            self._request_interceptors.append(interceptor)
            return self

        next_component = uri_components[0]
        if BaseRouteTeeNodeBuilder._is_pattern_component(next_component):
            self._pattern_route_builder = self._get_or_build_and_get_pattern_route_builder(next_component)
            return self._pattern_route_builder.get().add_request_interceptor(uri_components[1:], interceptor)

        self._sub_routes_builders[next_component] = self._get_or_build_and_get_sub_route_builder(next_component)
        return self._sub_routes_builders[next_component].add_request_interceptor(uri_components[1:], interceptor)

    def add_response_interceptor(self, uri_components, interceptor):
        if len(uri_components) == 0:
            self._response_interceptors.append(interceptor)
            return self

        next_component = uri_components[0]
        if BaseRouteTeeNodeBuilder._is_pattern_component(next_component):
            self._pattern_route_builder = self._get_or_build_and_get_pattern_route_builder(next_component)
            return self._pattern_route_builder.get().add_response_interceptor(uri_components[1:], interceptor)

        self._sub_routes_builders[next_component] = self._get_or_build_and_get_sub_route_builder(next_component)
        return self._sub_routes_builders[next_component].add_response_interceptor(uri_components[1:], interceptor)

    def add_handler(self, http_method, uri_components, handler):
        if len(uri_components) == 0:
            if http_method in self._handlers:
                raise DuplicateHandlerRoutesException("Cannot have two handlers with equal routes: {r}".format(r=http_method))
            self._handlers[http_method] = handler
            return self

        next_component = uri_components[0]
        if BaseRouteTeeNodeBuilder._is_pattern_component(next_component):
            self._pattern_route_builder = self._get_or_build_and_get_pattern_route_builder(next_component)
            return self._pattern_route_builder.get().add_handler(http_method, uri_components[1:], handler)

        self._sub_routes_builders[next_component] = self._get_or_build_and_get_sub_route_builder(next_component)
        return self._sub_routes_builders[next_component].add_handler(http_method, uri_components[1:], handler)

    @staticmethod
    def _is_pattern_component(uri_component):
        return uri_component.startswith("{") and uri_component.endswith("}")

    def _get_or_build_and_get_pattern_route_builder(self, uri_component):
        return Optional.of(self._pattern_route_builder.get_or_default(PatternRouteTreeNodeBuilder(uri_component[1:-1])))

    def _get_or_build_and_get_sub_route_builder(self, uri_component):
        return self._sub_routes_builders.get(uri_component, RouteTreeNodeBuilder())


class PatternRouteTreeNodeBuilder(BaseRouteTeeNodeBuilder):

    def __init__(self, pattern_name):
        super().__init__()
        self._pattern_name = pattern_name

    def build(self):
        return PatternRouteTreeNode(
            self._pattern_name,
            {uri_component: node_builder.build() for uri_component, node_builder in self._sub_routes_builders.items()},
            self._request_interceptors,
            self._handlers,
            self._response_interceptors,
            self._pattern_route_builder.map(lambda rb: rb.build()))


class RouteTreeNodeBuilder(BaseRouteTeeNodeBuilder):

    def build(self):
        return RouteTreeNode(
            {uri_component: node_builder.build() for uri_component, node_builder in self._sub_routes_builders.items()},
            self._request_interceptors,
            self._handlers,
            self._response_interceptors,
            self._pattern_route_builder.map(lambda rb: rb.build()))


class DuplicateHandlerRoutesException(Exception):
    pass


class HandlerNotFoundException(Exception):
    pass




