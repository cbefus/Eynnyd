import unittest
from src.routing.routes_builder import RoutesBuilder
from src.utils.request_uri import RequestURI
from src.eynnyd_webapp import EynnydWebappBuilder
from src.request import AbstractRequest
from src.response import ResponseBuilder


class TestEynnydWebapp(unittest.TestCase):

    class StubRequest(AbstractRequest):

        def __init__(
                self,
                method="GET",
                request_uri="/",
                headers=None,
                client_ip_address="127.0.0.1",
                cookies=None,
                query_parameters=None,
                path_parameters=None,
                byte_body=b"",
                utf8_body=""):
            self._method = method
            self._request_uri = RequestURI("http", "localhost", 8000, request_uri, "")
            self._headers = {} if not headers else headers
            self._ip_address = client_ip_address
            self._cookies = {} if not cookies else cookies
            self._query_params = {} if not query_parameters else query_parameters
            self._path_params = {} if not path_parameters else path_parameters
            self._byte_body = byte_body
            self._utf8_body = utf8_body

        def copy_and_set_path_parameters(self, path_parameters):
            return TestEynnydWebapp.StubRequest(
                method=self.http_method,
                request_uri=self.request_uri.path,
                headers=self.headers,
                client_ip_address=self.client_ip_address,
                cookies=self.cookies,
                query_parameters=self.query_parameters,
                path_parameters=path_parameters,
                byte_body=self.byte_body,
                utf8_body=self.utf8_body)

        @property
        def http_method(self):
            return self._method

        @property
        def request_uri(self):
            return self._request_uri

        @property
        def forwarded_request_uri(self):
            return self._request_uri

        @property
        def headers(self):
            return self._headers

        @property
        def client_ip_address(self):
            return self._ip_address

        @property
        def cookies(self):
            return self._cookies

        @property
        def query_parameters(self):
            return self._query_params

        @property
        def path_parameters(self):
            return self._path_params

        @property
        def byte_body(self):
            return self._byte_body

        @property
        def utf8_body(self):
            return self._utf8_body

    class SpyHandler:

        def __init__(self):
            self._handler_call_count = 0

        @property
        def handler_call_count(self):
            return self._handler_call_count

        def test_handler(self, request):
            self._handler_call_count += 1
            return ResponseBuilder().set_body("PANTS!").build()

    def test_base_level_handler(self):

        spy_handler = TestEynnydWebapp.SpyHandler()
        routes = RoutesBuilder().add_handler("GET", "/", spy_handler.test_handler).build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebapp.StubRequest(method="GET", request_uri="/")
        response = test_app.process_request_to_response(request)

        self.assertEqual(1, spy_handler.handler_call_count)
        self.assertEqual("PANTS!", response.body)

    def test_base_handler_selection_by_method(self):
        pass

    def test_simple_pathed_handler(self):
        pass

    def test_simple_pathed_handler_selection(self):
        pass

    def test_simple_pathed_handler_selection_by_method(self):
        pass

    def test_pattern_pathed_handler(self):
        pass

    def test_pattern_pathed_handler_selection_follows_direct_match(self):
        pass

    def test_pattern_pathed_handler_selection_by_method(self):
        pass

    def test_request_interceptors_called_in_order(self):
        pass

    def test_response_interceptors_called_in_order(self):
        pass

    def test_error_handlers_called(self):
        pass

    def test_error_handlers_called_in_order(self):
        pass








