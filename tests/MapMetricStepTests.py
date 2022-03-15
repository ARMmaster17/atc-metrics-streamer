import unittest

from dto.CacheMetricsDTO import CacheMetricsDTO
from etl.Pipeline import Pipeline
from etl.PipelineStep import PipelineStep
from steps.MapMetricStep import MapMetricStep


class MockPipelineSetupStep(PipelineStep):
    def __init__(self):
        super().__init__(self.__class__.__name__)

    def run_step(self, pipeline_context):
        mock_payload = {}
        mock_payload['mock_key'] = 'mock_value'
        mock_dto = CacheMetricsDTO(mock_payload)
        metrics = [mock_dto]
        pipeline_context.add_var('metrics_list', metrics)

class MockVerifyPipelineStep(PipelineStep):
    def __init__(self, verify_key):
        super().__init__(self.__class__.__name__)
        self.__verify_key = verify_key
        self.__assert_flag = False

    def run_step(self, pipeline_context):
        self.__assert_flag = (pipeline_context.get_var('metrics_list')[0].get_metric_var(self.__verify_key) == 'mock_value')

    def get_assert_flag(self):
        return self.__assert_flag


class MapMetricsStepTests(unittest.TestCase):
    def test_step_maps_direct(self):
        pipeline = Pipeline()
        pipeline.add_step(MockPipelineSetupStep())
        pipeline.add_step(MapMetricStep('mock_key', 'mock_key'))
        verify_step = MockVerifyPipelineStep('mock_key')
        pipeline.add_step(verify_step)
        pipeline.run()
        self.assertEqual(verify_step.get_assert_flag(), True)

    def test_step_maps_rename(self):
        pipeline = Pipeline()
        pipeline.add_step(MockPipelineSetupStep())
        pipeline.add_step(MapMetricStep('mock_key', 'mock_key2'))
        verify_step = MockVerifyPipelineStep('mock_key2')
        pipeline.add_step(verify_step)
        pipeline.run()
        self.assertEqual(verify_step.get_assert_flag(), True)



if __name__ == '__main__':
    unittest.main()
