import unittest
from http import HTTPStatus
from src.routing.routes_builder import RoutesBuilder
from src.utils.http_status import HTTPStatusFactory
from src.utils.request_uri import RequestURI
from src.eynnyd_webapp import EynnydWebappBuilder
from src.request import AbstractRequest
from src.response import ResponseBuilder


class TestEynnydWebappHandlers(unittest.TestCase):

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
            return TestEynnydWebappHandlers.StubRequest(
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

        def __init__(self, body="PANTS!"):
            self._handler_call_count = 0
            self._request_path_params = {}
            self._body = body

        @property
        def handler_call_count(self):
            return self._handler_call_count

        @property
        def request_path_parameters(self):
            return self._request_path_params

        def test_handler(self, request):
            self._handler_call_count += 1
            self._request_path_params = request.path_parameters
            return ResponseBuilder().set_body(self._body).build()

    def test_base_level_handler(self):
        spy_handler = TestEynnydWebappHandlers.SpyHandler()
        routes = RoutesBuilder().add_handler("GET", "/", spy_handler.test_handler).build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="GET", request_uri="/")
        response = test_app.process_request_to_response(request)

        self.assertEqual(1, spy_handler.handler_call_count)
        self.assertEqual("PANTS!", response.body)

    def test_base_handler_selection_by_method(self):
        spy_get_handler = TestEynnydWebappHandlers.SpyHandler(body="NOPE")
        spy_post_handler = TestEynnydWebappHandlers.SpyHandler(body="YEP")
        routes = \
            RoutesBuilder()\
                .add_handler("GET", "/", spy_get_handler.test_handler)\
                .add_handler("POST", "/", spy_post_handler.test_handler)\
                .build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="POST", request_uri="/")
        response = test_app.process_request_to_response(request)

        self.assertEqual(1, spy_post_handler.handler_call_count)
        self.assertEqual(0, spy_get_handler.handler_call_count)
        self.assertEqual("YEP", response.body)

    def test_base_handler_404s_by_method(self):
        spy_get_handler = TestEynnydWebappHandlers.SpyHandler()
        spy_post_handler = TestEynnydWebappHandlers.SpyHandler()

        routes = \
            RoutesBuilder() \
                .add_handler("GET", "/", spy_get_handler.test_handler) \
                .add_handler("POST", "/", spy_post_handler.test_handler) \
                .build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="PUT", request_uri="/")
        response = test_app.process_request_to_response(request)

        self.assertEqual(0, spy_post_handler.handler_call_count)
        self.assertEqual(0, spy_get_handler.handler_call_count)
        self.assertEqual(HTTPStatusFactory.create(HTTPStatus.NOT_FOUND), response.status)

    def test_simple_pathed_handler(self):
        spy_handler = TestEynnydWebappHandlers.SpyHandler()
        routes = RoutesBuilder().add_handler("GET", "/foo/bar", spy_handler.test_handler).build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="GET", request_uri="/foo/bar")
        response = test_app.process_request_to_response(request)

        self.assertEqual(1, spy_handler.handler_call_count)
        self.assertEqual("PANTS!", response.body)

    def test_simple_pathed_handler_selection(self):
        spy_get_handler = TestEynnydWebappHandlers.SpyHandler("NOPE")
        spy_post_handler = TestEynnydWebappHandlers.SpyHandler("YEP")
        routes = \
            RoutesBuilder() \
                .add_handler("GET", "/foo/bar", spy_get_handler.test_handler) \
                .add_handler("POST", "/fizz/buzz", spy_post_handler.test_handler) \
                .build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="POST", request_uri="/fizz/buzz")
        response = test_app.process_request_to_response(request)

        self.assertEqual(1, spy_post_handler.handler_call_count)
        self.assertEqual(0, spy_get_handler.handler_call_count)
        self.assertEqual("YEP", response.body)

    def test_simple_pathed_handler_selection_by_method(self):
        spy_get_handler = TestEynnydWebappHandlers.SpyHandler("NOPE")
        spy_post_handler = TestEynnydWebappHandlers.SpyHandler("YEP")
        routes = \
            RoutesBuilder() \
                .add_handler("GET", "/foo/bar", spy_get_handler.test_handler) \
                .add_handler("POST", "/foo/bar", spy_post_handler.test_handler) \
                .build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="POST", request_uri="/foo/bar")
        response = test_app.process_request_to_response(request)

        self.assertEqual(1, spy_post_handler.handler_call_count)
        self.assertEqual(0, spy_get_handler.handler_call_count)
        self.assertEqual("YEP", response.body)

    def test_simple_pathed_handler_404s_by_path(self):
        spy_get_handler = TestEynnydWebappHandlers.SpyHandler("NOPE")
        spy_post_handler = TestEynnydWebappHandlers.SpyHandler("YEP")
        routes = \
            RoutesBuilder() \
                .add_handler("GET", "/foo/bar", spy_get_handler.test_handler) \
                .add_handler("POST", "/foo/bar", spy_post_handler.test_handler) \
                .build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="POST", request_uri="/foo/buzz")
        response = test_app.process_request_to_response(request)

        self.assertEqual(0, spy_post_handler.handler_call_count)
        self.assertEqual(0, spy_get_handler.handler_call_count)
        self.assertEqual(HTTPStatusFactory.create(HTTPStatus.NOT_FOUND), response.status)

    def test_simple_pathed_handler_404s_by_method(self):
        spy_get_handler = TestEynnydWebappHandlers.SpyHandler("NOPE")
        spy_post_handler = TestEynnydWebappHandlers.SpyHandler("YEP")
        routes = \
            RoutesBuilder() \
                .add_handler("GET", "/foo/bar", spy_get_handler.test_handler) \
                .add_handler("POST", "/foo/bar", spy_post_handler.test_handler) \
                .build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="PUT", request_uri="/foo/bar")
        response = test_app.process_request_to_response(request)

        self.assertEqual(0, spy_post_handler.handler_call_count)
        self.assertEqual(0, spy_get_handler.handler_call_count)
        self.assertEqual(HTTPStatusFactory.create(HTTPStatus.NOT_FOUND), response.status)

    def test_pattern_pathed_handler(self):
        spy_handler = TestEynnydWebappHandlers.SpyHandler()
        routes = RoutesBuilder().add_handler("GET", "/foo/{fid}", spy_handler.test_handler).build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="GET", request_uri="/foo/1234")
        response = test_app.process_request_to_response(request)

        self.assertEqual(1, spy_handler.handler_call_count)
        self.assertEqual("PANTS!", response.body)
        self.assertEqual(1, len(spy_handler.request_path_parameters))
        self.assertTrue("fid" in spy_handler.request_path_parameters)
        self.assertEqual("1234", spy_handler.request_path_parameters.get("fid"))

    def test_pattern_pathed_handler_nested(self):
        spy_handler = TestEynnydWebappHandlers.SpyHandler()
        routes = RoutesBuilder().add_handler("GET", "/foo/{fid}/fizz", spy_handler.test_handler).build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="GET", request_uri="/foo/1234/fizz")
        response = test_app.process_request_to_response(request)

        self.assertEqual(1, spy_handler.handler_call_count)
        self.assertEqual("PANTS!", response.body)
        self.assertEqual(1, len(spy_handler.request_path_parameters))
        self.assertTrue("fid" in spy_handler.request_path_parameters)
        self.assertEqual("1234", spy_handler.request_path_parameters.get("fid"))

    def test_pattern_pathed_handler_multiple(self):
        spy_handler = TestEynnydWebappHandlers.SpyHandler()
        routes = RoutesBuilder().add_handler("GET", "/foo/{fid}/bar/{bid}", spy_handler.test_handler).build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="GET", request_uri="/foo/1234/bar/987")
        response = test_app.process_request_to_response(request)

        self.assertEqual(1, spy_handler.handler_call_count)
        self.assertEqual("PANTS!", response.body)
        self.assertEqual(2, len(spy_handler.request_path_parameters))
        self.assertTrue("fid" in spy_handler.request_path_parameters)
        self.assertTrue("bid" in spy_handler.request_path_parameters)
        self.assertEqual("1234", spy_handler.request_path_parameters.get("fid"))
        self.assertEqual("987", spy_handler.request_path_parameters.get("bid"))

    def test_pattern_pathed_handler_selection_follows_direct_match(self):
        spy_direct_match_handler = TestEynnydWebappHandlers.SpyHandler("YEP")
        spy_pattern_handler = TestEynnydWebappHandlers.SpyHandler("NOPE")
        routes = \
            RoutesBuilder() \
                .add_handler("GET", "/foo/bar", spy_direct_match_handler.test_handler) \
                .add_handler("GET", "/foo/{fid}", spy_pattern_handler.test_handler) \
                .build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="GET", request_uri="/foo/bar")
        response = test_app.process_request_to_response(request)

        self.assertEqual(0, spy_pattern_handler.handler_call_count)
        self.assertEqual(1, spy_direct_match_handler.handler_call_count)
        self.assertEqual("YEP", response.body)

    def test_pattern_pathed_handler_selection_by_method(self):
        spy_get_handler = TestEynnydWebappHandlers.SpyHandler("NOPE")
        spy_post_handler = TestEynnydWebappHandlers.SpyHandler("YEP")
        routes = \
            RoutesBuilder() \
                .add_handler("GET", "/foo/{fid}", spy_get_handler.test_handler) \
                .add_handler("POST", "/foo/{fid}", spy_post_handler.test_handler) \
                .build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="POST", request_uri="/foo/1234")
        response = test_app.process_request_to_response(request)

        self.assertEqual(1, spy_post_handler.handler_call_count)
        self.assertEqual(0, spy_get_handler.handler_call_count)
        self.assertEqual("YEP", response.body)
        self.assertEqual(1, len(spy_post_handler.request_path_parameters))
        self.assertEqual(0, len(spy_get_handler.request_path_parameters))
        self.assertTrue("fid" in spy_post_handler.request_path_parameters)
        self.assertEqual("1234", spy_post_handler.request_path_parameters.get("fid"))


class TestEynnydWebappInterceptors(unittest.TestCase):

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
            return TestEynnydWebappHandlers.StubRequest(
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
            self._request_path_params = {}

        @property
        def handler_call_count(self):
            return self._handler_call_count

        def test_handler(self, request):
            self._handler_call_count += 1
            return ResponseBuilder().set_body(request._utf8_body+"HANDLER").build()

    class SpyRequestInterceptor:

        def __init__(self, body_append=""):
            self._call_count = 0
            self._body_append = body_append

        @property
        def interceptor_call_count(self):
            return self._call_count

        def test_interceptor(self, request):
            self._call_count += 1
            request._utf8_body += self._body_append
            return request

    def test_request_interceptors_called_in_order(self):
        spy_root_interceptor = TestEynnydWebappInterceptors.SpyRequestInterceptor(body_append="ROOT")
        spy_foo_interceptor = TestEynnydWebappInterceptors.SpyRequestInterceptor(body_append="FOO")
        spy_foo_id_interceptor = TestEynnydWebappInterceptors.SpyRequestInterceptor(body_append="FID")

        spy_post_handler = TestEynnydWebappInterceptors.SpyHandler()

        routes = \
            RoutesBuilder() \
                .add_request_interceptor("/", spy_root_interceptor.test_interceptor) \
                .add_request_interceptor("/foo", spy_foo_interceptor.test_interceptor) \
                .add_request_interceptor("/foo/{fid}", spy_foo_id_interceptor.test_interceptor) \
                .add_handler("POST", "/foo/{fid}", spy_post_handler.test_handler) \
                .build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="POST", request_uri="/foo/1234")
        response = test_app.process_request_to_response(request)
        self.assertEqual(1, spy_root_interceptor.interceptor_call_count)
        self.assertEqual(1, spy_foo_interceptor.interceptor_call_count)
        self.assertEqual(1, spy_foo_id_interceptor.interceptor_call_count)
        self.assertEqual(1, spy_post_handler.handler_call_count)
        self.assertEqual("ROOTFOOFIDHANDLER", response.body)

    def test_request_interceptors_not_called_when_not_around_path(self):
        spy_root_interceptor = TestEynnydWebappInterceptors.SpyRequestInterceptor(body_append="ROOT")
        spy_bar_interceptor = TestEynnydWebappInterceptors.SpyRequestInterceptor(body_append="FOO")
        spy_bar_id_interceptor = TestEynnydWebappInterceptors.SpyRequestInterceptor(body_append="FID")

        spy_post_handler = TestEynnydWebappInterceptors.SpyHandler()

        routes = \
            RoutesBuilder() \
                .add_request_interceptor("/", spy_root_interceptor.test_interceptor) \
                .add_request_interceptor("/bar", spy_bar_interceptor.test_interceptor) \
                .add_request_interceptor("/bar/{fid}", spy_bar_id_interceptor.test_interceptor) \
                .add_handler("POST", "/foo/{fid}", spy_post_handler.test_handler) \
                .build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="POST", request_uri="/foo/1234")
        response = test_app.process_request_to_response(request)
        self.assertEqual(1, spy_root_interceptor.interceptor_call_count)
        self.assertEqual(0, spy_bar_interceptor.interceptor_call_count)
        self.assertEqual(0, spy_bar_id_interceptor.interceptor_call_count)
        self.assertEqual(1, spy_post_handler.handler_call_count)
        self.assertEqual("ROOTHANDLER", response.body)

    def test_response_interceptors_called_in_order(self):
        pass

    def test_response_interceptors_not_called_when_not_around_path(self):
        pass

    def test_error_handlers_called(self):
        pass

    def test_generic_error_handler_called(self):
        pass








