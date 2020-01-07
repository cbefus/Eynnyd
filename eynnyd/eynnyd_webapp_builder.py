from optional import Optional

from eynnyd.exceptions import EynnydWebappBuildException
from eynnyd.internal.eynnyd_webapp import EynnydWebapp
from eynnyd.error_handlers_builder import ErrorHandlersBuilder


class EynnydWebappBuilder:

    def __init__(self):
        self._routes = Optional.empty()
        self._error_handlers = ErrorHandlersBuilder().build()

    def set_routes(self, root_tree_node):
        """
        Sets routes built by the Eynnyd RoutesBuilder

        :param root_tree_node: the result from the Eynnyd RoutesBuilder build method
        :return: This builder so that fluent design can be used.
        """
        self._routes = Optional.of(root_tree_node)
        return self

    def set_error_handlers(self, error_handlers):
        """
        Sets the error handlers built by Eynnyd ErrorHandlersBuilder
        :param error_handlers: the result from the Eynnyd ErrorHandlersBuilder create method
        :return: This builder so that fluent design can be used
        """
        self._error_handlers = error_handlers
        return self

    def build(self):
        """
        Builds the webapp

        :return: the WSGI compliant webapp
        """
        return EynnydWebapp(
            self._routes.get_or_raise(EynnydWebappBuildException(
                "You must set routes for the webapp to route requests too.")),
            self._error_handlers)