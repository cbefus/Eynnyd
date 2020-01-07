
from eynnyd.internal.routing.pattern_route import PatternRoute


class PatternRouteBuilder:

    def __init__(self, parameter_name, pattern_route_node_builder):
        self._parameter_name = parameter_name
        self._pattern_route_node_builder = pattern_route_node_builder

    @property
    def pattern_route_node_builder(self):
        return self._pattern_route_node_builder

    def build(self):
        return PatternRoute(self._parameter_name, self._pattern_route_node_builder.build())
