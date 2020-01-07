from eynnyd.exceptions import HandlerNotFoundException


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
