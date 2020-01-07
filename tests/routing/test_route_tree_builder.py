from unittest import TestCase

from eynnyd.exceptions import DuplicateHandlerRoutesException
from eynnyd.internal.routing.route_tree_builder import RouteTeeBuilder


class TestRouteTeeBuilder(TestCase):

    def test_cant_add_duplicate_handler_routes(self):
        def fake_handler(request):
            pass

        def another_fake_handler(request):
            pass

        builder = RouteTeeBuilder()
        builder.add_handler("GET", ["foo", "bar"], fake_handler)
        with self.assertRaises(DuplicateHandlerRoutesException):
            builder.add_handler("GET", ["foo", "bar"], another_fake_handler)
