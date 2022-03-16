from datetime import datetime, timezone, timedelta

from etl.PipelineStep import PipelineStep


class TransformTimestampsStep(PipelineStep):
    def __init__(self):
        super().__init__(self.__class__.__name__, dependencies=['metrics_list'])

    def run_step(self, pipeline_context):
        new_metrics = []
        for metric in pipeline_context.get_var('metrics_list'):
            metric.set_metric_var('check_time', datetime.now(timezone.utc).isoformat())
            metric.set_metric_var('next_check', (datetime.now(timezone.utc) + timedelta(seconds=10)).isoformat())
            new_metrics.append(metric)
        pipeline_context.add_var('metrics_list', new_metrics)