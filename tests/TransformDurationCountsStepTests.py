import unittest

from dto.CacheMetricsDTO import CacheMetricsDTO
from etl.Pipeline import Pipeline
from etl.PipelineContext import PipelineContext
from etl.PipelineStep import PipelineStep
from steps.TransformDurationCountsStep import TransformDurationCountsStep

class MockPipelineSetupStep(PipelineStep):
    def __init__(self):
        super().__init__(self.__class__.__name__, provides=['metrics_list'])

    def run_step(self, pipeline_context: PipelineContext):
        metrics = []
        mock_metric = CacheMetricsDTO(None, None, None)
        mock_metric.set_metric_var('test_ms', 1)
        metrics.append(mock_metric)
        pipeline_context.add_var('metrics_list', metrics)

class MockVerifyPipelineStep(PipelineStep):
    def __init__(self, verify_key: str):
        super().__init__(self.__class__.__name__, dependencies=['metrics_list'])
        self.__verify_key = verify_key
        self.__assert_flag = False

    def run_step(self, pipeline_context: PipelineContext):
        self.__assert_flag = (pipeline_context.get_var('metrics_list')[0].get_metric_var(self.__verify_key) == 1000)

    def get_assert_flag(self):
        return self.__assert_flag

class TransformDurationCountsStepTests(unittest.TestCase):
    def test_step_loads(self):
        step = TransformDurationCountsStep('test_ms')
        self.assertIsNotNone(step)

    def test_step_creates_field(self):
        pipeline = Pipeline()
        pipeline.add_step(MockPipelineSetupStep())
        pipeline.add_step(TransformDurationCountsStep('test_ms'))
        pipeline.add_step(MockVerifyPipelineStep('test_us'), load_step=True)
        pipeline.run()

    def test_step_converts_to_us(self):
        pipeline = Pipeline()
        pipeline.add_step(MockPipelineSetupStep())
        pipeline.add_step(TransformDurationCountsStep('test_ms'))
        verify_step = MockVerifyPipelineStep('test_us')
        pipeline.add_step(verify_step, load_step=True)
        pipeline.run()
        self.assertTrue(verify_step.get_assert_flag())


if __name__ == '__main__':
    unittest.main()
