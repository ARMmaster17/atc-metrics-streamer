import unittest

from etl.Pipeline import Pipeline
from etl.PipelineStep import PipelineStep

class MockScheduleStepA(PipelineStep):
    def __init__(self):
        super().__init__(self.__class__.__name__, provides=["test_var"])

    def run_step(self, pipeline_context):
        pipeline_context.add_var("test_var", "test_value")


class MockScheduleStepB(PipelineStep):
    def __init__(self):
        super().__init__(self.__class__.__name__, dependencies=["test_var"])
        self.__assert_flag = False

    def get_assert_flag(self):
        return self.__assert_flag

    def run_step(self, pipeline_context):
        if pipeline_context.get_var("test_var") == "test_value":
            self.__assert_flag = True

class PipelineSchedulerTests(unittest.TestCase):
    def test_schedules_basic_dependency_in_order(self):
        pipeline = Pipeline()
        step_a = MockScheduleStepA()
        step_b = MockScheduleStepB()
        pipeline.add_step(step_a)
        pipeline.add_step(step_b)
        pipeline.run()
        self.assertTrue(step_b.get_assert_flag())

    def test_schedules_basic_dependency_out_of_order(self):
        pipeline = Pipeline()
        step_a = MockScheduleStepA()
        step_b = MockScheduleStepB()
        pipeline.add_step(step_b)
        pipeline.add_step(step_a)
        pipeline.run()
        self.assertTrue(step_b.get_assert_flag())


if __name__ == '__main__':
    unittest.main()
