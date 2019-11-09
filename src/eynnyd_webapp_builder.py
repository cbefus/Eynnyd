from optional import Optional

from src.exceptions import EynnydWebappBuildException
from src.eynnyd_webapp import EynnydWebapp
from src.plan_execution.exception_handlers_registry import ExceptionHandlersRegistry


class EynnydWebappBuilder:

    def __init__(self):
        self._routes = Optional.empty()
        self._exception_handlers = ExceptionHandlersRegistry().create()

    def set_routes(self, root_tree_node):
        self._routes = Optional.of(root_tree_node)
        return self

    def set_error_handlers(self, exception_handlers):
        self._exception_handlers = exception_handlers
        return self

    def build(self):
        return EynnydWebapp(
            self._routes.get_or_raise(EynnydWebappBuildException(
                "You must set routes for the webapp to route requests too.")),
            self._exception_handlers)