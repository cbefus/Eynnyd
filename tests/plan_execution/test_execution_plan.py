import unittest

from eynnyd.internal.plan_execution.execution_plan_builder import ExecutionPlanBuilder
from eynnyd.exceptions import ExecutionPlanBuildException


class TestExecutionPlanBuilder(unittest.TestCase):

    def test_simplest_plan(self):
        plan = ExecutionPlanBuilder().set_handler("something").build()
        self.assertEqual("something", plan.handler)
        self.assertEqual(0, len(plan.request_interceptors))
        self.assertEqual(0, len(plan.response_interceptors))
        self.assertEqual(0, len(plan.path_parameters))

    def test_plan_raises_without_handler(self):
        with self.assertRaises(ExecutionPlanBuildException):
            ExecutionPlanBuilder().build()

    def test_adding_request_interceptors(self):
        plan = \
            ExecutionPlanBuilder()\
                .set_handler("something")\
                .add_request_interceptors(["a", "b"])\
                .add_request_interceptors(["c"])\
                .build()
        self.assertEqual("something", plan.handler)
        self.assertEqual(3, len(plan.request_interceptors))
        self.assertEqual(0, len(plan.response_interceptors))
        self.assertEqual(0, len(plan.path_parameters))

    def test_adding_response_interceptors(self):
        plan = \
            ExecutionPlanBuilder() \
                .set_handler("something") \
                .add_response_interceptors(["a", "b"]) \
                .add_response_interceptors(["c"]) \
                .build()
        self.assertEqual("something", plan.handler)
        self.assertEqual(0, len(plan.request_interceptors))
        self.assertEqual(3, len(plan.response_interceptors))
        self.assertEqual(0, len(plan.path_parameters))

    def test_adding_path_parameters(self):
        plan = \
            ExecutionPlanBuilder() \
                .set_handler("something") \
                .add_path_parameter("a", "b") \
                .add_path_parameter("c", "d") \
                .build()
        self.assertEqual("something", plan.handler)
        self.assertEqual(0, len(plan.request_interceptors))
        self.assertEqual(0, len(plan.response_interceptors))
        self.assertEqual(2, len(plan.path_parameters))
        self.assertTrue("a" in plan.path_parameters)
        self.assertTrue("c" in plan.path_parameters)
        self.assertEqual("b", plan.path_parameters.get("a"))
        self.assertEqual("d", plan.path_parameters.get("c"))

