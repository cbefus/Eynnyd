from unittest import TestCase

from eynnyd.exceptions import RouteBuildException, NonCallableInterceptor, \
    NonCallableHandler, CallbackIncorrectNumberOfParametersException
from eynnyd.routes_builder import RoutesBuilder


class TestRoutesBuilder(TestCase):

    def test_add_uncallable_request_interceptor_raises(self):
        builder = RoutesBuilder()
        with self.assertRaises(NonCallableInterceptor):
            builder.add_request_interceptor("/foo/bar", "not callable")

    def test_add_too_few_param_request_interceptor_raises(self):
        def test_interceptor():
            pass

        builder = RoutesBuilder()
        with self.assertRaises(CallbackIncorrectNumberOfParametersException):
            builder.add_request_interceptor("/foo/bar", test_interceptor)

    def test_add_too_many_param_request_interceptor_raises(self):
        def test_interceptor(one_param, two_many_param):
            pass

        builder = RoutesBuilder()
        with self.assertRaises(CallbackIncorrectNumberOfParametersException):
            builder.add_request_interceptor("/foo/bar", test_interceptor)

    def test_add_request_interceptor_on_repeating_path_param_name_raises(self):
        def test_interceptor(one_param):
            pass

        builder = RoutesBuilder()
        with self.assertRaises(RouteBuildException):
            builder.add_request_interceptor("/foo/{bar}/123/{bar}", test_interceptor)

    def test_add_uncallable_response_interceptor_raises(self):
        builder = RoutesBuilder()
        with self.assertRaises(NonCallableInterceptor):
            builder.add_response_interceptor("/foo/bar", "not callable")

    def test_add_too_few_param_response_interceptor_raises(self):
        def test_interceptor(one_param):
            pass

        builder = RoutesBuilder()
        with self.assertRaises(CallbackIncorrectNumberOfParametersException):
            builder.add_response_interceptor("/foo/bar", test_interceptor)

    def test_add_too_many_param_response_interceptor_raises(self):
        def test_interceptor(one_param, two_param, three_many_param):
            pass

        builder = RoutesBuilder()
        with self.assertRaises(CallbackIncorrectNumberOfParametersException):
            builder.add_response_interceptor("/foo/bar", test_interceptor)

    def test_add_response_interceptor_on_repeating_path_param_name_raises(self):
        def test_interceptor(one_param, two_param):
            pass

        builder = RoutesBuilder()
        with self.assertRaises(RouteBuildException):
            builder.add_response_interceptor("/foo/{bar}/123/{bar}", test_interceptor)

    def test_add_uncallable_handler_raises(self):
        builder = RoutesBuilder()
        with self.assertRaises(NonCallableHandler):
            builder.add_handler("GET", "/foo/bar", "not callable")

    def test_add_too_few_param_handler_raises(self):
        def test_handler():
            pass

        builder = RoutesBuilder()
        with self.assertRaises(CallbackIncorrectNumberOfParametersException):
            builder.add_handler("GET", "/foo/bar", test_handler)

    def test_add_too_many_param_handler_raises(self):
        def test_handler(one_param, two_param):
            pass

        builder = RoutesBuilder()
        with self.assertRaises(CallbackIncorrectNumberOfParametersException):
            builder.add_handler("GET", "/foo/bar", test_handler)

    def test_add_handler_on_repeating_path_param_name_raises(self):
        def test_handler(one_param):
            pass

        builder = RoutesBuilder()
        with self.assertRaises(RouteBuildException):
            builder.add_handler("GET", "/foo/{bar}/123/{bar}", test_handler)

    def test_add_duplicate_route_handler_raises(self):
        def test_handler(one_param):
            pass

        def test_another_handler(one_param):
            pass

        builder = RoutesBuilder()
        builder.add_handler("GET", "/foo/bar", test_handler)
        with self.assertRaises(RouteBuildException):
            builder.add_handler("GET", "/foo/bar", test_another_handler)
