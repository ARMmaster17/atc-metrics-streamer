import logging
import unittest

from etl.PipelineStep import PipelineStep
from etl.Pipeline import Pipeline


class MockStep(PipelineStep):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.__run_count = 0

    def get_run_count(self):
        return self.__run_count

    def run_step(self, pipeline_context):
        self.__run_count += 1


class MockExceptionStep(PipelineStep):
    def __init__(self):
        super().__init__(self.__class__.__name__)

    def run_step(self, pipeline_context):
        raise Exception("Mock Exception")


class PipelineTestCase(unittest.TestCase):
    def test_pipeline_initializes(self):
        pipeline = Pipeline()

    def test_pipeline_runs_empty(self):
        pipeline = Pipeline()
        pipeline.run()

    def test_pipeline_runs_with_benchmark_debug(self):
        pipeline = Pipeline()
        with self.assertLogs(logging.getLogger(), level=logging.DEBUG) as cm:
            pipeline.run()
        self.assertEqual(1, len(cm.records))

    def test_pipeline_runs_with_one_step(self):
        pipeline = Pipeline()
        step = MockStep()
        pipeline.add_step(step)
        pipeline.run()
        self.assertEqual(step.get_run_count(), 1)

    def test_steps_run_with_benchmark_debug(self):
        pipeline = Pipeline()
        step = MockStep()
        pipeline.add_step(step)
        with self.assertLogs(logging.getLogger(), level=logging.DEBUG) as cm:
            pipeline.run()
        self.assertEqual(2, len(cm.records))

    def test_pipeline_captures_exceptions(self):
        pipeline = Pipeline()
        pipeline.add_step(MockExceptionStep())
        pipeline.run()


if __name__ == '__main__':
    unittest.main()
