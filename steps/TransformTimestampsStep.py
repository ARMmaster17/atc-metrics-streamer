from datetime import datetime, timezone, timedelta

from watergrid.context import DataContext
from watergrid.steps import Step


class TransformTimestampsStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__, requires=['metrics_list'])

    def run(self, pipeline_context: DataContext):
        new_metrics = []
        for metric in pipeline_context.get('metrics_list'):
            metric.set_metric_var('check_time', datetime.now(timezone.utc).isoformat())
            metric.set_metric_var('next_check', (datetime.now(timezone.utc) + timedelta(seconds=10)).isoformat())
            new_metrics.append(metric)
        pipeline_context.set('metrics_list', new_metrics)