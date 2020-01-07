import unittest
from http import HTTPStatus

from eynnyd.routes_builder import RoutesBuilder
from eynnyd.error_handlers_builder import ErrorHandlersBuilder
from eynnyd.internal.utils.request_uri import RequestURI
from eynnyd.eynnyd_webapp_builder import EynnydWebappBuilder
from eynnyd.abstract_request import AbstractRequest
from eynnyd.response_builder import ResponseBuilder
from eynnyd.exceptions import RouteNotFoundException
from eynnyd.internal.response_body import ResponseBody


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
            return ResponseBuilder().set_utf8_body(self._body).build()

    def test_base_level_handler(self):
        spy_handler = TestEynnydWebappHandlers.SpyHandler()
        routes = RoutesBuilder().add_handler("GET", "/", spy_handler.test_handler).build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="GET", request_uri="/")
        response = test_app.process_request_to_response(request)

        self.assertEqual(1, spy_handler.handler_call_count)
        self.assertEqual(b"PANTS!", response.body.content)

    def test_base_handler_selection_by_method(self):
        spy_get_handler = TestEynnydWebappHandlers.SpyHandler(body="NOPE")
        spy_post_handler = TestEynnydWebappHandlers.SpyHandler(body="YEP")
        routes = \
            RoutesBuilder() \
                .add_handler("GET", "/", spy_get_handler.test_handler) \
                .add_handler("POST", "/", spy_post_handler.test_handler) \
                .build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="POST", request_uri="/")
        response = test_app.process_request_to_response(request)

        self.assertEqual(1, spy_post_handler.handler_call_count)
        self.assertEqual(0, spy_get_handler.handler_call_count)
        self.assertEqual(b"YEP", response.body.content)

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
        self.assertEqual(HTTPStatus.NOT_FOUND.value, response.status.code)

    def test_simple_pathed_handler(self):
        spy_handler = TestEynnydWebappHandlers.SpyHandler()
        routes = RoutesBuilder().add_handler("GET", "/foo/bar", spy_handler.test_handler).build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="GET", request_uri="/foo/bar")
        response = test_app.process_request_to_response(request)

        self.assertEqual(1, spy_handler.handler_call_count)
        self.assertEqual(b"PANTS!", response.body.content)

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
        self.assertEqual(b"YEP", response.body.content)

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
        self.assertEqual(b"YEP", response.body.content)

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
        self.assertEqual(HTTPStatus.NOT_FOUND.value, response.status.code)

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
        self.assertEqual(HTTPStatus.NOT_FOUND.value, response.status.code)

    def test_pattern_pathed_handler(self):
        spy_handler = TestEynnydWebappHandlers.SpyHandler()
        routes = RoutesBuilder().add_handler("GET", "/foo/{fid}", spy_handler.test_handler).build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="GET", request_uri="/foo/1234")
        response = test_app.process_request_to_response(request)

        self.assertEqual(1, spy_handler.handler_call_count)
        self.assertEqual(b"PANTS!", response.body.content)
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
        self.assertEqual(b"PANTS!", response.body.content)
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
        self.assertEqual(b"PANTS!", response.body.content)
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
        self.assertEqual(b"YEP", response.body.content)

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
        self.assertEqual(b"YEP", response.body.content)
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
            return ResponseBuilder().set_utf8_body(request._utf8_body + "HANDLER").build()

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

    class SpyResponseInterceptor:

        def __init__(self, body_append=""):
            self._call_count = 0
            self._body_append = body_append

        @property
        def interceptor_call_count(self):
            return self._call_count

        def test_interceptor(self, request, response):
            self._call_count += 1
            response._body = \
                ResponseBody(response._body.type, response._body.content + self._body_append.encode("utf-8"))
            return response

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
        self.assertEqual(b"ROOTFOOFIDHANDLER", response.body.content)

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
        self.assertEqual(b"ROOTHANDLER", response.body.content)

    def test_response_interceptors_called_in_order(self):
        spy_root_interceptor = TestEynnydWebappInterceptors.SpyResponseInterceptor(body_append="ROOT")
        spy_foo_interceptor = TestEynnydWebappInterceptors.SpyResponseInterceptor(body_append="FOO")
        spy_foo_id_interceptor = TestEynnydWebappInterceptors.SpyResponseInterceptor(body_append="FID")

        spy_post_handler = TestEynnydWebappInterceptors.SpyHandler()

        routes = \
            RoutesBuilder() \
                .add_handler("POST", "/foo/{fid}", spy_post_handler.test_handler) \
                .add_response_interceptor("/foo/{fid}", spy_foo_id_interceptor.test_interceptor) \
                .add_response_interceptor("/foo", spy_foo_interceptor.test_interceptor) \
                .add_response_interceptor("/", spy_root_interceptor.test_interceptor) \
                .build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="POST", request_uri="/foo/1234")
        response = test_app.process_request_to_response(request)
        self.assertEqual(1, spy_post_handler.handler_call_count)
        self.assertEqual(1, spy_root_interceptor.interceptor_call_count)
        self.assertEqual(1, spy_foo_interceptor.interceptor_call_count)
        self.assertEqual(1, spy_foo_id_interceptor.interceptor_call_count)
        self.assertEqual(b"HANDLERFIDFOOROOT", response.body.content)

    def test_response_interceptors_not_called_when_not_around_path(self):
        spy_root_interceptor = TestEynnydWebappInterceptors.SpyResponseInterceptor(body_append="ROOT")
        spy_bar_interceptor = TestEynnydWebappInterceptors.SpyResponseInterceptor(body_append="FOO")
        spy_bar_id_interceptor = TestEynnydWebappInterceptors.SpyResponseInterceptor(body_append="FID")

        spy_post_handler = TestEynnydWebappInterceptors.SpyHandler()

        routes = \
            RoutesBuilder() \
                .add_handler("POST", "/foo/{fid}", spy_post_handler.test_handler) \
                .add_response_interceptor("/bar/{fid}", spy_bar_id_interceptor.test_interceptor) \
                .add_response_interceptor("/", spy_root_interceptor.test_interceptor) \
                .add_response_interceptor("/bar", spy_bar_interceptor.test_interceptor) \
                .build()
        test_app = EynnydWebappBuilder().set_routes(routes).build()
        request = TestEynnydWebappHandlers.StubRequest(method="POST", request_uri="/foo/1234")
        response = test_app.process_request_to_response(request)
        self.assertEqual(1, spy_root_interceptor.interceptor_call_count)
        self.assertEqual(0, spy_bar_interceptor.interceptor_call_count)
        self.assertEqual(0, spy_bar_id_interceptor.interceptor_call_count)
        self.assertEqual(1, spy_post_handler.handler_call_count)
        self.assertEqual(b"HANDLERROOT", response.body.content)


class TestEynnydWebappErrorHandlers(unittest.TestCase):
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

    class StubRaisesHandler:

        def __init__(self, exception_to_throw):
            self._exception_to_throw = exception_to_throw

        def test_handler(self, request):
            raise self._exception_to_throw("BOOM!!")

    class StubHandler:

        def test_handler(self, request):
            return ResponseBuilder().build()

    class StubRaisesRequestInterceptor:

        def __init__(self, exception_to_throw):
            self._exception_to_throw = exception_to_throw

        def test_interceptor(self, request):
            raise self._exception_to_throw("BOOM!!")

    class StubRaisesResponseInterceptor:

        def __init__(self, exception_to_throw):
            self._exception_to_throw = exception_to_throw

        def test_interceptor(self, request, response):
            raise self._exception_to_throw("BOOM!!")

    class SpyExceptionHandler:

        def __init__(self):
            self._call_count = 0

        @property
        def call_count(self):
            return self._call_count

        def test_pre_response_handler(self, exc, request):
            self._call_count += 1
            return ResponseBuilder() \
                .set_status(HTTPStatus.BAD_REQUEST) \
                .set_utf8_body("Big Boom") \
                .build()

        def test_post_response_handler(self, exc, request, response):
            self._call_count += 1
            return ResponseBuilder() \
                .set_status(HTTPStatus.BAD_REQUEST) \
                .set_utf8_body("Big Boom") \
                .build()

    def test_error_handle_from_handler_called(self):
        class BoomException(Exception):
            pass

        stub_raises_handler = TestEynnydWebappErrorHandlers.StubRaisesHandler(BoomException)
        spy_boom_exception_handler = TestEynnydWebappErrorHandlers.SpyExceptionHandler()
        spy_generic_exception_handler = TestEynnydWebappErrorHandlers.SpyExceptionHandler()

        routes = \
            RoutesBuilder() \
                .add_handler("GET", "/boom", stub_raises_handler.test_handler) \
                .build()

        error_handlers = \
            ErrorHandlersBuilder() \
                .add_pre_response_error_handler(
                    BoomException,
                    spy_boom_exception_handler.test_pre_response_handler) \
                .add_pre_response_error_handler(
                    Exception,
                    spy_generic_exception_handler.test_pre_response_handler) \
                .build()

        test_app = EynnydWebappBuilder().set_routes(routes).set_error_handlers(error_handlers).build()
        request = TestEynnydWebappHandlers.StubRequest(method="GET", request_uri="/boom")
        response = test_app.process_request_to_response(request)
        self.assertEqual(HTTPStatus.BAD_REQUEST.value, response.status.code)
        self.assertEqual(1, spy_boom_exception_handler.call_count)
        self.assertEqual(0, spy_generic_exception_handler.call_count)

    def test_error_handler_from_request_interceptor(self):
        class BoomException(Exception):
            pass

        stub_raises_request_handler = TestEynnydWebappErrorHandlers.StubRaisesRequestInterceptor(BoomException)

        stub_raises_handler = TestEynnydWebappErrorHandlers.StubRaisesHandler(Exception)
        spy_boom_exception_handler = TestEynnydWebappErrorHandlers.SpyExceptionHandler()
        spy_generic_exception_handler = TestEynnydWebappErrorHandlers.SpyExceptionHandler()

        routes = \
            RoutesBuilder() \
                .add_request_interceptor("/", stub_raises_request_handler.test_interceptor) \
                .add_handler("GET", "/boom", stub_raises_handler.test_handler) \
                .build()

        error_handlers = \
            ErrorHandlersBuilder() \
                .add_pre_response_error_handler(
                    BoomException,
                    spy_boom_exception_handler.test_pre_response_handler) \
                .add_pre_response_error_handler(
                    Exception,
                    spy_generic_exception_handler.test_pre_response_handler) \
                .build()

        test_app = EynnydWebappBuilder().set_routes(routes).set_error_handlers(error_handlers).build()
        request = TestEynnydWebappHandlers.StubRequest(method="GET", request_uri="/boom")
        response = test_app.process_request_to_response(request)
        self.assertEqual(HTTPStatus.BAD_REQUEST.value, response.status.code)
        self.assertEqual(1, spy_boom_exception_handler.call_count)
        self.assertEqual(0, spy_generic_exception_handler.call_count)

    def test_error_handler_from_response_interceptor(self):
        class BoomException(Exception):
            pass

        stub_raises_response_handler = TestEynnydWebappErrorHandlers.StubRaisesResponseInterceptor(BoomException)

        stub_handler = TestEynnydWebappErrorHandlers.StubHandler()
        spy_boom_exception_handler = TestEynnydWebappErrorHandlers.SpyExceptionHandler()
        spy_generic_exception_handler = TestEynnydWebappErrorHandlers.SpyExceptionHandler()

        routes = \
            RoutesBuilder() \
                .add_handler("GET", "/noboom", stub_handler.test_handler) \
                .add_response_interceptor("/", stub_raises_response_handler.test_interceptor) \
                .build()

        error_handlers = \
            ErrorHandlersBuilder() \
                .add_post_response_error_handler(
                    BoomException,
                    spy_boom_exception_handler.test_post_response_handler) \
                .add_post_response_error_handler(
                    Exception,
                    spy_generic_exception_handler.test_post_response_handler) \
                .build()

        test_app = EynnydWebappBuilder().set_routes(routes).set_error_handlers(error_handlers).build()
        request = TestEynnydWebappHandlers.StubRequest(method="GET", request_uri="/noboom")
        response = test_app.process_request_to_response(request)
        self.assertEqual(HTTPStatus.BAD_REQUEST.value, response.status.code)
        self.assertEqual(1, spy_boom_exception_handler.call_count)
        self.assertEqual(0, spy_generic_exception_handler.call_count)

    def test_not_found_exception_handler(self):
        stub_raises_handler = TestEynnydWebappErrorHandlers.StubRaisesHandler(Exception)
        spy_not_found_exception_handler = TestEynnydWebappErrorHandlers.SpyExceptionHandler()
        spy_generic_exception_handler = TestEynnydWebappErrorHandlers.SpyExceptionHandler()

        routes = \
            RoutesBuilder() \
                .add_handler("GET", "/boom", stub_raises_handler.test_handler) \
                .build()

        error_handlers = \
            ErrorHandlersBuilder() \
                .add_pre_response_error_handler(
                    RouteNotFoundException,
                    spy_not_found_exception_handler.test_pre_response_handler) \
                .add_pre_response_error_handler(
                    Exception,
                    spy_generic_exception_handler.test_pre_response_handler) \
                .build()

        test_app = EynnydWebappBuilder().set_routes(routes).set_error_handlers(error_handlers).build()
        request = TestEynnydWebappHandlers.StubRequest(method="GET", request_uri="/route_does_not_exist")
        response = test_app.process_request_to_response(request)
        self.assertEqual(HTTPStatus.BAD_REQUEST.value, response.status.code)
        self.assertEqual(1, spy_not_found_exception_handler.call_count)
        self.assertEqual(0, spy_generic_exception_handler.call_count)

    def test_generic_error_handler_fallthrough_called(self):
        class NotRegisteredException(Exception):
            pass

        class BoomException(Exception):
            pass

        stub_raises_handler = TestEynnydWebappErrorHandlers.StubRaisesHandler(NotRegisteredException)
        spy_boom_exception_handler = TestEynnydWebappErrorHandlers.SpyExceptionHandler()
        spy_generic_exception_handler = TestEynnydWebappErrorHandlers.SpyExceptionHandler()

        routes = \
            RoutesBuilder() \
                .add_handler("GET", "/boom", stub_raises_handler.test_handler) \
                .build()

        error_handlers = \
            ErrorHandlersBuilder() \
                .add_pre_response_error_handler(
                    BoomException,
                    spy_boom_exception_handler.test_pre_response_handler) \
                .add_pre_response_error_handler(
                    Exception,
                    spy_generic_exception_handler.test_pre_response_handler) \
                .build()

        test_app = EynnydWebappBuilder().set_routes(routes).set_error_handlers(error_handlers).build()
        request = TestEynnydWebappHandlers.StubRequest(method="GET", request_uri="/boom")
        response = test_app.process_request_to_response(request)
        self.assertEqual(HTTPStatus.BAD_REQUEST.value, response.status.code)
        self.assertEqual(0, spy_boom_exception_handler.call_count)
        self.assertEqual(1, spy_generic_exception_handler.call_count)



