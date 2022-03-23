from watergrid.context import DataContext
from watergrid.steps import Step


class TransformSummaryInfoStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__, requires=['metrics_list'])

    def run(self, pipeline_context: DataContext):
        new_metrics = []
        for metric in pipeline_context.get('metrics_list'):
            is_up = metric.get_raw_payload_var('combined_available')
            summary_stats = {
                'up': float(2 if is_up else 0),
                'down': float(0 if is_up else 2),
            }
            metric.set_metric_var('summary', summary_stats)
            new_metrics.append(metric)
        pipeline_context.set('metrics_list', new_metrics)