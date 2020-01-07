import unittest
import logging

from eynnyd.internal.plan_execution.execution_plan import ExecutionPlan
from eynnyd.internal.plan_execution.plan_executor import PlanExecutor
from eynnyd.exceptions import RequestInterceptorReturnedNonRequestException, HandlerReturnedNonResponseException, \
    ResponseInterceptorReturnedNonResponseException
from eynnyd.abstract_request import AbstractRequest
from eynnyd.response_builder import ResponseBuilder
from http import HTTPStatus
from eynnyd.error_handlers_builder import ErrorHandlersBuilder

LOG = logging.getLogger("test_plan_executor")


class TestPlanExecutor(unittest.TestCase):

    def test_execute_plan_exceptions_in_request_interceptors_run_pre_response_error_handler(self):
        class CustomException(Exception):
            pass

        def fake_interceptor(original_request):
            raise CustomException("Just a test")

        def error_handler(thrown_error, request):
            return ResponseBuilder().set_status(HTTPStatus.SERVICE_UNAVAILABLE).build()

        exception_handlers = \
            ErrorHandlersBuilder()\
                .add_pre_response_error_handler(CustomException, error_handler)\
                .build()
        plan_executor = PlanExecutor(exception_handlers)

        plan = ExecutionPlan([fake_interceptor], "some handler", [], {})
        response = plan_executor.execute_plan(plan, "original test request")
        self.assertEqual(HTTPStatus.SERVICE_UNAVAILABLE.value, response.status.code)

    def test_execute_plan_exception_in_handler_run_pre_response_error_handler(self):
        class CustomException(Exception):
            pass

        def fake_handler(some_request):
            raise CustomException("Just a test")

        def error_handler(thrown_error, request):
            return ResponseBuilder().set_status(HTTPStatus.SERVICE_UNAVAILABLE).build()

        exception_handlers = \
            ErrorHandlersBuilder()\
                .add_pre_response_error_handler(CustomException, error_handler)\
                .build()
        plan_executor = PlanExecutor(exception_handlers)

        plan = ExecutionPlan([], fake_handler, [], {})
        response = plan_executor.execute_plan(plan, "original test request")
        self.assertEqual(HTTPStatus.SERVICE_UNAVAILABLE.value, response.status.code)

    def test_execute_plan_exception_in_response_interceptor_runs_post_response_error_handler(self):
        class CustomException(Exception):
            pass

        def fake_interceptor(original_request, original_response):
            raise CustomException("Just a test")

        def error_handler(thrown_error, request, response):
            return ResponseBuilder().set_status(HTTPStatus.SERVICE_UNAVAILABLE).build()

        def fake_handler(request):
            return ResponseBuilder().set_status(HTTPStatus.OK).build()

        exception_handlers = \
            ErrorHandlersBuilder()\
                .add_post_response_error_handler(CustomException, error_handler)\
                .build()
        plan_executor = PlanExecutor(exception_handlers)

        plan = ExecutionPlan([], fake_handler, [fake_interceptor], {})
        response = plan_executor.execute_plan(plan, "original test request")
        self.assertEqual(HTTPStatus.SERVICE_UNAVAILABLE.value, response.status.code)

    def test_execute_plan_executes_request_interceptors_handler_and_response_interceptors_correctly(self):
        class FakeRequest(AbstractRequest):
            def __init__(self, http_method):
                self._http_method = http_method

            @property
            def http_method(self):
                return self._http_method

            @property
            def request_uri(self):
                pass

            @property
            def forwarded_request_uri(self):
                pass

            @property
            def headers(self):
                pass

            @property
            def client_ip_address(self):
                pass

            @property
            def cookies(self):
                pass

            @property
            def query_parameters(self):
                pass

            @property
            def path_parameters(self):
                pass

            @property
            def byte_body(self):
                pass

            @property
            def utf8_body(self):
                pass

        def fake_request_interceptor_first(request):
            self.assertEqual("GET", request.http_method)
            return FakeRequest("POST")

        def fake_request_interceptor_second(request):
            self.assertEqual("POST", request.http_method)
            return FakeRequest("PUT")

        def fake_handler(request):
            self.assertEqual("PUT", request.http_method)
            return ResponseBuilder().set_status(HTTPStatus.OK).build()

        def fake_response_interceptor_first(request, response):
            self.assertEqual("PUT", request.http_method)
            self.assertEqual(HTTPStatus.OK.value, response.status.code)
            return ResponseBuilder().set_status(HTTPStatus.ACCEPTED).build()

        def fakse_response_interceptor_second(request, response):
            self.assertEqual("PUT", request.http_method)
            self.assertEqual(HTTPStatus.ACCEPTED.value, response.status.code)
            return ResponseBuilder().set_status(HTTPStatus.CREATED).build()

        plan_executor = PlanExecutor(ErrorHandlersBuilder().build())
        plan = \
            ExecutionPlan(
                [fake_request_interceptor_first, fake_request_interceptor_second],
                fake_handler,
                [fakse_response_interceptor_second, fake_response_interceptor_first],
                {})
        response = plan_executor.execute_plan(plan, FakeRequest("GET"))
        self.assertEqual(HTTPStatus.CREATED.value, response.status.code)

    def test_execute_plan_with_non_request_returning_request_interceptor_raises(self):
        def fake_interceptor(original_request):
            return "not a proper request - should throw"

        def correct_error_thrown_handler(thrown_error, request):
            return ResponseBuilder().set_status(HTTPStatus.SERVICE_UNAVAILABLE).build()

        exception_handlers = \
            ErrorHandlersBuilder()\
                .add_pre_response_error_handler(
                    RequestInterceptorReturnedNonRequestException,
                    correct_error_thrown_handler)\
                .build()
        plan_executor = PlanExecutor(exception_handlers)

        plan = ExecutionPlan([fake_interceptor], "some handler", [], {})
        response = plan_executor.execute_plan(plan, "original test request")
        self.assertEqual(HTTPStatus.SERVICE_UNAVAILABLE.value, response.status.code)

    def test_execute_plan_request_interceptors_swap_out_request(self):
        class FakeRequest(AbstractRequest):

            @property
            def http_method(self):
                return "PUT"

            @property
            def request_uri(self):
                pass

            @property
            def forwarded_request_uri(self):
                pass

            @property
            def headers(self):
                pass

            @property
            def client_ip_address(self):
                pass

            @property
            def cookies(self):
                pass

            @property
            def query_parameters(self):
                pass

            @property
            def path_parameters(self):
                pass

            @property
            def byte_body(self):
                pass

            @property
            def utf8_body(self):
                pass

        def fake_interceptor(original_request):
            return FakeRequest()

        def fake_handler(request):
            self.assertEqual("PUT", request.http_method)
            return ResponseBuilder().set_status(HTTPStatus.OK).build()

        plan_executor = PlanExecutor(ErrorHandlersBuilder().build())
        plan = ExecutionPlan([fake_interceptor], fake_handler, [], {})
        response = plan_executor.execute_plan(plan, "original test request")
        self.assertEqual(HTTPStatus.OK.value, response.status.code)

    def test_execute_plan_non_response_returning_handlers_raises(self):
        def fake_handler(some_request):
            return "not a proper response - should throw"

        def correct_error_thrown_handler(thrown_error, request):
            return ResponseBuilder().set_status(HTTPStatus.SERVICE_UNAVAILABLE).build()

        exception_handlers = \
            ErrorHandlersBuilder()\
                .add_pre_response_error_handler(HandlerReturnedNonResponseException, correct_error_thrown_handler)\
                .build()
        plan_executor = PlanExecutor(exception_handlers)

        plan = ExecutionPlan([], fake_handler, [], {})
        response = plan_executor.execute_plan(plan, "original test request")
        self.assertEqual(HTTPStatus.SERVICE_UNAVAILABLE.value, response.status.code)

    def test_execute_plan_handler_sets_the_response(self):

        def fake_handler(some_request):
            return ResponseBuilder().set_status(HTTPStatus.ACCEPTED).build()

        plan_executor = PlanExecutor(ErrorHandlersBuilder().build())
        plan = ExecutionPlan([], fake_handler, [], {})
        response = plan_executor.execute_plan(plan, "original test request")
        self.assertEqual(HTTPStatus.ACCEPTED.value, response.status.code)

    def test_execute_plan_non_response_returing_response_interceptor_raises(self):

        def fake_interceptor(original_request, original_response):
            return "not a proper response - should throw"

        def correct_error_thrown_handler(thrown_error, request, response):
            return ResponseBuilder().set_status(HTTPStatus.SERVICE_UNAVAILABLE).build()

        def fake_handler(request):
            return ResponseBuilder().set_status(HTTPStatus.OK).build()

        exception_handlers = \
            ErrorHandlersBuilder()\
                .add_post_response_error_handler(
                    ResponseInterceptorReturnedNonResponseException,
                    correct_error_thrown_handler)\
                .build()
        plan_executor = PlanExecutor(exception_handlers)

        plan = ExecutionPlan([], fake_handler, [fake_interceptor], {})
        response = plan_executor.execute_plan(plan, "original test request")
        self.assertEqual(HTTPStatus.SERVICE_UNAVAILABLE.value, response.status.code)

    def test_execute_plan_response_interceptors_swaps_the_response(self):
        def fake_handler(request):
            return ResponseBuilder().set_status(HTTPStatus.OK).build()

        def fake_interceptor(original_request, original_response):
            return ResponseBuilder().set_status(HTTPStatus.ACCEPTED).build()

        plan_executor = PlanExecutor(ErrorHandlersBuilder().build())
        plan = ExecutionPlan([], fake_handler, [fake_interceptor], {})
        response = plan_executor.execute_plan(plan, "original test request")
        self.assertEqual(HTTPStatus.ACCEPTED.value, response.status.code)
