import inspect

from src.routing.route_tree_builder import RouteTeeBuilder
from src.exceptions import DuplicateHandlerRoutesException, RouteBuildException, NonCallableInterceptor, \
    NonCallableHandler, CallbackIncorrectNumberOfParametersException
from src.utils.uri_components_converter import URIComponentsConverter


class RoutesBuilder:

    def __init__(self):
        self._route_tree_builder = RouteTeeBuilder()

    def add_request_interceptor(self, uri_path, interceptor):
        if not hasattr(interceptor, '__call__'):
            raise NonCallableInterceptor(
                "Request Interceptor for path {u} is not callable.".format(u=uri_path))
        if 1 != len(inspect.signature(interceptor).parameters):
            raise CallbackIncorrectNumberOfParametersException(
                "Request Interceptor {n} for path {u} does not take exactly 1 argument (the request)"
                    .format(u=uri_path, n=interceptor.__name__))

        components = URIComponentsConverter.from_uri(uri_path)
        RoutesBuilder._validate_path_has_unique_parameter_names_or_raise(components)
        self._route_tree_builder.add_request_interceptor(components, interceptor)
        return self

    def add_response_interceptor(self, uri_path, interceptor):
        if not hasattr(interceptor, '__call__'):
            raise NonCallableInterceptor(
                "Response Interceptor for path {u} is not callable.".format(u=uri_path))
        if 2 != len(inspect.signature(interceptor).parameters):
            raise CallbackIncorrectNumberOfParametersException(
                "Response Interceptor {n} for path {u} does not take exactly 2 argument (the request and response)"
                    .format(u=uri_path, n=interceptor.__name__))

        components = URIComponentsConverter.from_uri(uri_path)
        RoutesBuilder._validate_path_has_unique_parameter_names_or_raise(components)
        self._route_tree_builder.add_response_interceptor(components, interceptor)
        return self

    def add_handler(self, http_method, uri_path, handler):
        if not hasattr(handler, '__call__'):
            raise NonCallableHandler(
                "Handler for method {m} on path {u} is not callable.".format(m=http_method, u=uri_path))
        if 1 != len(inspect.signature(handler).parameters):
            raise CallbackIncorrectNumberOfParametersException(
                "Handler {n} for method {m} on path {u} does not take exactly 1 argument (the request)"
                    .format(u=uri_path, n=handler.__name__, m=http_method))
        components = URIComponentsConverter.from_uri(uri_path)
        RoutesBuilder._validate_path_has_unique_parameter_names_or_raise(components)
        try:
            self._route_tree_builder.add_handler(http_method, components, handler)
        except DuplicateHandlerRoutesException as e:
            raise RouteBuildException(
                "Error while trying to add handler to route {u}, method: {m}".format(u=uri_path, m=http_method),
                e)
        return self

    def build(self):
        return self._route_tree_builder.build()

    @staticmethod
    def _validate_path_has_unique_parameter_names_or_raise(uri_components):
        path_parameter_names = set()
        for path_component in uri_components:
            if path_component in path_parameter_names:
                raise RouteBuildException("Multiple uses of same path parameter name in uri: {u}".format(u="/" + "/".join(uri_components)))

            if path_component.startswith("{") and path_component.endswith("}"):
                path_parameter_names.add(path_component)


