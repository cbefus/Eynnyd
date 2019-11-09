

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
