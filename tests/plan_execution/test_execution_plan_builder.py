import unittest

from eynnyd.internal.plan_execution.execution_plan_builder import ExecutionPlanBuilder
from eynnyd.exceptions import ExecutionPlanBuildException


class TestExecutionPlanBuilder(unittest.TestCase):

    def test_build_without_handler_raises(self):
        with self.assertRaises(ExecutionPlanBuildException):
            ExecutionPlanBuilder().build()

    def test_builder_builds_correct_plan(self):
        built_plan = \
            ExecutionPlanBuilder()\
                .add_path_parameter("foo", "bar")\
                .add_path_parameter("fizz", "buzz")\
                .add_request_interceptors(["first", "second"])\
                .add_request_interceptors(["third"])\
                .add_response_interceptors(["uno", "dos"])\
                .add_response_interceptors(["tres"])\
                .set_handler("handler")\
                .build()
        self.assertDictEqual({"foo": "bar", "fizz": "buzz"}, built_plan.path_parameters)
        self.assertListEqual(["first", "second", "third"], built_plan.request_interceptors)
        self.assertListEqual(["uno", "dos", "tres"], built_plan.response_interceptors)
        self.assertEqual("handler", built_plan.handler)
