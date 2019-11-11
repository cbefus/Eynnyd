from optional import Optional

from src.exceptions import EynnydWebappBuildException
from src.internal.eynnyd_webapp import EynnydWebapp
from src.exception_handlers_registry import ExceptionHandlersRegistry


class EynnydWebappBuilder:

    def __init__(self):
        self._routes = Optional.empty()
        self._exception_handlers = ExceptionHandlersRegistry().create()

    def set_routes(self, root_tree_node):
        """
        Sets routes built by the Eynnyd RoutesBuilder

        :param root_tree_node: the result from the Eynnyd RoutesBuilder build method
        :return: This builder so that fluent design can be used.
        """
        self._routes = Optional.of(root_tree_node)
        return self

    def set_error_handlers(self, exception_handlers):
        """
        Sets the error handlers built by Eynnyd ExceptionHandlersRegistry
        :param exception_handlers: the result from the Eynnyd ExceptionHandlersRegistry create method
        :return: This builder so that fluent design can be used
        """
        self._exception_handlers = exception_handlers
        return self

    def build(self):
        """
        Builds the webapp

        :return: the WSGI compliant webapp
        """
        return EynnydWebapp(
            self._routes.get_or_raise(EynnydWebappBuildException(
                "You must set routes for the webapp to route requests too.")),
            self._exception_handlers)