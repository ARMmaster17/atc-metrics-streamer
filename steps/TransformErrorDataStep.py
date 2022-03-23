from watergrid.context import DataContext
from watergrid.steps import Step


class TransformErrorDataStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__, requires=['metrics_list'])

    def run(self, pipeline_context: DataContext):
        new_metrics = []
        for metric in pipeline_context.get('metrics_list'):
            is_up = metric.get_raw_payload_var('combined_available')
            if not is_up:
                error_struct = {
                    'message': metric.get_raw_payload_var('status'),
                    'type': "astats"
                }
                metric.set_metric_var('error', error_struct)
            new_metrics.append(metric)
        pipeline_context.set('metrics_list', new_metrics)