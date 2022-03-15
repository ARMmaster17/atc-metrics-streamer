import unittest

from etl.Pipeline import Pipeline
from etl.PipelineContext import PipelineContext
from etl.PipelineStep import PipelineStep


class MockContextStep(PipelineStep):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.__assert_flag = False

    def get_assert_flag(self):
        return self.__assert_flag

    def run_step(self, pipeline_context):
        if pipeline_context is not None:
            self.__assert_flag = True


class PipelineContextTests(unittest.TestCase):
    def test_create_context(self):
        context = PipelineContext()
        self.assertIsNotNone(context)

    def test_place_var(self):
        context = PipelineContext()
        context.add_var("test", "testvalue")
        self.assertEqual(context.get_var("test"), "testvalue")

    def test_can_use_context_in_pipeline(self):
        pipeline = Pipeline()
        step = MockContextStep()
        pipeline.add_step(step)
        pipeline.run()
        self.assertTrue(step.get_assert_flag())


if __name__ == '__main__':
    unittest.main()
