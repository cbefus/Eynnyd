import unittest
from http import HTTPStatus

from src.plan_execution.default_exception_handlers import default_invalid_cookie_header_exception_handler, \
    default_internal_server_error_exception_handler_only_request, default_internal_server_error_exception_handler, \
    default_route_not_found_exception_handler


class TestDefaultExceptionHandlers(unittest.TestCase):

    def test_default_not_found_exception_returns_404(self):
        class FakeRequest:
            @property
            def http_method(self):
                return "fake http method"

            @property
            def request_uri(self):
                return "fake request uri"
        response = default_route_not_found_exception_handler(Exception(), FakeRequest())
        self.assertEqual(HTTPStatus.NOT_FOUND, response.status)

    def test_default_invalid_cookie_header_exception_returns_400(self):
        class FakeRequest:
            @property
            def headers(self):
                return {"COOKIE": "fake cookie"}

        response = default_invalid_cookie_header_exception_handler(Exception(), FakeRequest())
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status)

    def test_default_internal_server_error_exception_request_only_returns_500(self):
        response = default_internal_server_error_exception_handler_only_request(Exception(), "fake request")
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, response.status)

    def test_default_internal_server_error_exception_returns_500(self):
        response = default_internal_server_error_exception_handler(Exception(), "fake request", "fake response")
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, response.status)


