from src.routing.route_tree import RouteTreeNodeBuilder
from src.exceptions import DuplicateHandlerRoutesException, RouteBuildException
from src.utils.uri_components_converter import URIComponentsConverter


class RoutesBuilder:

    def __init__(self):
        self._root_node_builder = RouteTreeNodeBuilder()

    def add_request_interceptor(self, uri_path, interceptor):
        # TODO: validate interceptor is runnable
        # TODO: validate interceptor runs given a fake request
        # TODO: validate interceptor returns something matching a request
        components = URIComponentsConverter.from_uri(uri_path)
        RoutesBuilder._validate_path_has_unique_parameter_names_or_raise(components)
        self._root_node_builder.add_request_interceptor(components, interceptor)
        return self

    def add_handler(self, http_method, uri_path, handler):
        # TODO: validate http_method (One of GET/POST/etc)
        # TODO: validate handler is runnable
        # TODO: validate handler runs given a fake request
        # TODO: validate handler returns something matching a response
        components = URIComponentsConverter.from_uri(uri_path)
        RoutesBuilder._validate_path_has_unique_parameter_names_or_raise(components)
        try:
            self._root_node_builder.add_handler(http_method, components, handler)
        except DuplicateHandlerRoutesException as e:
            raise RouteBuildException(
                "Error while trying to add handler to route {u}, method: {m}".format(u=uri_path, m=http_method),
                e)
        return self

    def add_response_interceptor(self, uri_path, interceptor):
        # TODO: validate interceptor is runnable
        # TODO: validate interceptor runs given a fake request and fake response
        # TODO: validate interceptor returns something matching a response
        components = URIComponentsConverter.from_uri(uri_path)
        RoutesBuilder._validate_path_has_unique_parameter_names_or_raise(components)
        self._root_node_builder.add_response_interceptor(components, interceptor)
        return self

    def build(self):
        return self._root_node_builder.build()

    @staticmethod
    def _validate_path_has_unique_parameter_names_or_raise(uri_components):
        path_parameter_names = set()
        for path_component in uri_components:
            if path_component in path_parameter_names:
                raise RouteBuildException("Multiple uses of same path parameter name in uri: {u}".format(u="/" + "/".join(uri_components)))

            if path_component.startswith("{") and path_component.endswith("}"):
                path_parameter_names.add(path_component)


