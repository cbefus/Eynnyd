import unittest

from src.plan_execution.execution_plan import ExecutionPlan
from src.plan_execution.plan_executor import PlanExecutor
from src.exceptions import RequestInterceptorReturnedNonRequestException, HandlerReturnedNonResponseException, \
    ResponseInterceptorReturnedNonResponseException
from src.request import AbstractRequest
from src.response import ResponseBuilder
from http import HTTPStatus


class TestPlanExecutor(unittest.TestCase):

    def test_execute_request_interceptors_raises_on_non_request_return(self):
        def fake_interceptor(original_request):
            return "not a proper request - should throw"

        plan = ExecutionPlan([fake_interceptor], "some handler", [], {})
        with self.assertRaises(RequestInterceptorReturnedNonRequestException):
            PlanExecutor.execute_request_interceptors(plan, "original test request")

    def test_execute_request_interceptors_swaps_the_request(self):
        class FakeRequest(AbstractRequest):
            def copy_and_set_path_parameters(self, path_parameters):
                pass

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

        def fake_handler(some_request):
            return ResponseBuilder().set_status(HTTPStatus.OK).build()

        plan = ExecutionPlan([fake_interceptor], "some handler", [], {})
        new_request = PlanExecutor.execute_request_interceptors(plan, "original test request")
        self.assertEqual("PUT", new_request.http_method)

    def test_execute_handler_raises_on_non_response_return(self):
        def fake_handler(some_request):
            return "not a proper response - should throw"

        plan = ExecutionPlan([], fake_handler, [], {})
        with self.assertRaises(HandlerReturnedNonResponseException):
            PlanExecutor.execute_handler(plan, "original test request")

    def test_execute_handler_sets_the_response(self):

        def fake_handler(some_request):
            return ResponseBuilder().set_status(HTTPStatus.ACCEPTED).build()

        plan = ExecutionPlan([], fake_handler, [], {})
        response = PlanExecutor.execute_handler(plan, "original test request")
        self.assertEqual(HTTPStatus.ACCEPTED, response.status)

    def test_execute_response_interceptors_raises_on_non_response_return(self):

        def fake_interceptor(original_request, original_response):
            return "not a proper response - should throw"

        plan = ExecutionPlan([], "some fake handler", [fake_interceptor], {})
        with self.assertRaises(ResponseInterceptorReturnedNonResponseException):
            PlanExecutor.execute_response_interceptors(
                plan,
                "original test request",
                ResponseBuilder().set_status(HTTPStatus.OK).build())

    def test_execute_response_interceptors_swaps_the_response(self):
        def fake_interceptor(original_request, original_response):
            return ResponseBuilder().set_status(HTTPStatus.ACCEPTED).build()

        plan = ExecutionPlan([], "some fake handler", [fake_interceptor], {})
        response = \
            PlanExecutor.execute_response_interceptors(
                plan,
                "original test request",
                ResponseBuilder().set_status(HTTPStatus.OK).build())
        self.assertEqual(HTTPStatus.ACCEPTED, response.status)
