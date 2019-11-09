import unittest
from http import HTTPStatus

from src.response_builder import ResponseBuilder
from src.exceptions import ExceptionHandlingRegisterException, RouteNotFoundException, \
    CallbackIncorrectNumberOfParametersException, NonCallableExceptionHandlerException, \
    InvalidCookieHeaderException
from src.exception_handlers_registry import ExceptionHandlersRegistry


class TestExceptionHandlersRegistry(unittest.TestCase):

    def test_pre_response_handler_not_callable_raises(self):
        registry = ExceptionHandlersRegistry()
        with self.assertRaises(NonCallableExceptionHandlerException):
            registry.register_pre_response_error_handler(Exception, "not callable thing")

    def test_pre_response_handler_takes_too_few_args_raies(self):
        def fake_handler(only_one_arg):
            pass

        registry = ExceptionHandlersRegistry()
        with self.assertRaises(CallbackIncorrectNumberOfParametersException):
            registry.register_pre_response_error_handler(Exception, fake_handler)

    def test_pre_response_handler_takes_too_many_args(self):
        def fake_handler(one_arg, two_arg, three_too_many_arg):
            pass

        registry = ExceptionHandlersRegistry()
        with self.assertRaises(CallbackIncorrectNumberOfParametersException):
            registry.register_pre_response_error_handler(Exception, fake_handler)

    def test_pre_response_handler_exception_already_registered_raises(self):
        def fake_handler(one_arg, two_arg):
            pass

        registry = ExceptionHandlersRegistry()
        registry.register_pre_response_error_handler(Exception, fake_handler)
        with self.assertRaises(ExceptionHandlingRegisterException):
            registry.register_pre_response_error_handler(Exception, fake_handler)

    def test_pre_response_handler_has_default_route_not_found_error_handler(self):
        class FakeRequest:
            @property
            def http_method(self):
                return "fake http method"

            @property
            def request_uri(self):
                return "fake request uri"

        exception_handlers = ExceptionHandlersRegistry().create()
        response = exception_handlers.handle_pre_response_error(RouteNotFoundException(), FakeRequest())
        self.assertEqual(HTTPStatus.NOT_FOUND.value, response.status.code)

    def test_pre_response_handler_can_override_default_route_not_found_error_handler(self):
        class FakeRequest:
            @property
            def http_method(self):
                return "fake http method"

            @property
            def request_uri(self):
                return "fake request uri"

        def fake_handler(thrown_exc, request):
            return ResponseBuilder().set_status(HTTPStatus.OK).build()

        exception_handlers = \
            ExceptionHandlersRegistry()\
                .register_pre_response_error_handler(RouteNotFoundException, fake_handler)\
                .create()
        response = exception_handlers.handle_pre_response_error(RouteNotFoundException(), FakeRequest())
        self.assertEqual(HTTPStatus.OK.value, response.status.code)

    def test_pre_response_handler_has_default_invalid_cookie_error_handler(self):
        class FakeRequest:
            @property
            def headers(self):
                return {"COOKIE": "fake cookie"}

        exception_handlers = ExceptionHandlersRegistry().create()
        response = exception_handlers.handle_pre_response_error(InvalidCookieHeaderException(), FakeRequest())
        self.assertEqual(HTTPStatus.BAD_REQUEST.value, response.status.code)

    def test_pre_response_handler_can_override_default_invalid_cookie_error_handler(self):
        class FakeRequest:
            @property
            def headers(self):
                return {"COOKIE": "fake cookie"}

        def fake_handler(thrown_exc, request):
            return ResponseBuilder().set_status(HTTPStatus.OK).build()

        exception_handlers = \
            ExceptionHandlersRegistry()\
                .register_pre_response_error_handler(InvalidCookieHeaderException, fake_handler)\
                .create()
        response = exception_handlers.handle_pre_response_error(InvalidCookieHeaderException(), FakeRequest())
        self.assertEqual(HTTPStatus.OK.value, response.status.code)

    def test_pre_response_handler_has_default_internal_server_error_handler(self):
        exception_handlers = ExceptionHandlersRegistry().create()
        response = exception_handlers.handle_pre_response_error(Exception(), "fake request")
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR.value, response.status.code)

    def test_pre_response_handler_can_override_default_internal_server_error_handler(self):
        def fake_handler(thrown_exc, request):
            return ResponseBuilder().set_status(HTTPStatus.OK).build()

        exception_handlers = \
            ExceptionHandlersRegistry().register_pre_response_error_handler(Exception, fake_handler).create()
        response = exception_handlers.handle_pre_response_error(Exception(), "fake request")
        self.assertEqual(HTTPStatus.OK.value, response.status.code)

    def test_pre_response_handler_gets_registered(self):
        class FakeException(Exception):
            pass

        def fake_handler(thrown_exc, request):
            return ResponseBuilder().set_status(HTTPStatus.OK).build()

        exception_handlers = \
            ExceptionHandlersRegistry().register_pre_response_error_handler(FakeException, fake_handler).create()
        response = exception_handlers.handle_pre_response_error(FakeException(), "fake request")
        self.assertEqual(HTTPStatus.OK.value, response.status.code)

    def test_post_response_handler_not_callable_raises(self):
        registry = ExceptionHandlersRegistry()
        with self.assertRaises(NonCallableExceptionHandlerException):
            registry.register_post_response_error_handler(Exception, "not callable thing")

    def test_post_response_handler_takes_too_few_args_raies(self):
        def fake_handler(one_arg, only_two_args):
            pass

        registry = ExceptionHandlersRegistry()
        with self.assertRaises(CallbackIncorrectNumberOfParametersException):
            registry.register_post_response_error_handler(Exception, fake_handler)

    def test_post_response_handler_takes_too_many_args(self):
        def fake_handler(one_arg, two_arg, three_arg, four_too_many_arg):
            pass

        registry = ExceptionHandlersRegistry()
        with self.assertRaises(CallbackIncorrectNumberOfParametersException):
            registry.register_post_response_error_handler(Exception, fake_handler)

    def test_post_response_handler_exception_already_registered_raises(self):
        def fake_handler(one_arg, two_arg, three_arg):
            pass

        registry = ExceptionHandlersRegistry()
        registry.register_post_response_error_handler(Exception, fake_handler)
        with self.assertRaises(ExceptionHandlingRegisterException):
            registry.register_post_response_error_handler(Exception, fake_handler)

    def test_post_response_handler_has_default_internal_server_error_handler(self):
        exception_handlers = ExceptionHandlersRegistry().create()
        response = exception_handlers.handle_post_response_error(Exception(), "fake request", "fake response")
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR.value, response.status.code)

    def test_post_response_handler_can_override_default_internal_server_error_handler(self):
        def fake_handler(thrown_exc, request, response):
            return ResponseBuilder().set_status(HTTPStatus.OK).build()

        exception_handlers = \
            ExceptionHandlersRegistry().register_post_response_error_handler(Exception, fake_handler).create()
        response = exception_handlers.handle_post_response_error(Exception(), "fake request", "fake response")
        self.assertEqual(HTTPStatus.OK.value, response.status.code)

    def test_post_response_handler_gets_registered(self):
        class FakeException(Exception):
            pass

        def fake_handler(thrown_exc, request, response):
            return ResponseBuilder().set_status(HTTPStatus.OK).build()

        exception_handlers = \
            ExceptionHandlersRegistry().register_post_response_error_handler(FakeException, fake_handler).create()
        response = exception_handlers.handle_post_response_error(FakeException(), "fake request", "fake response")
        self.assertEqual(HTTPStatus.OK.value, response.status.code)
