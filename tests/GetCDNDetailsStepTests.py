import unittest

from etl.Pipeline import Pipeline
from etl.PipelineStep import PipelineStep
from steps.BuildCDNListStep import BuildCDNListStep
from steps.BuildTOConnectionInfoStep import BuildTOConnectionInfoStep
from steps.GetCDNDetailsStep import GetCDNDetailsStep


class MockCDNDetailListCheckStep(PipelineStep):
    def __init__(self):
        super().__init__(self.__class__.__name__, dependencies=["cdn_detail_list"])
        self.__assert_flag = False

    def get_assert_flag(self):
        return self.__assert_flag

    def run_step(self, pipeline_context):
        if len(pipeline_context.get_var("cdn_detail_list")) > 0:
            self.__assert_flag = True


class GetCDNDetailsStepTests(unittest.TestCase):
    def test_step_runs(self):
        pipeline = Pipeline()
        pipeline.add_step(BuildTOConnectionInfoStep())
        pipeline.add_step(BuildCDNListStep())
        pipeline.add_step(GetCDNDetailsStep())
        check_step = MockCDNDetailListCheckStep()
        pipeline.add_step(check_step)
        pipeline.run()
        self.assertTrue(check_step.get_assert_flag())


if __name__ == '__main__':
    unittest.main()
