from etl.PipelineStep import PipelineStep


class TransformErrorDataStep(PipelineStep):
    def __init__(self):
        super().__init__(self.__class__.__name__, dependencies=['metrics_list'])

    def run_step(self, pipeline_context):
        new_metrics = []
        for metric in pipeline_context.get_var('metrics_list'):
            is_up = metric.get_raw_payload_var('combined_available')
            if not is_up:
                error_struct = {
                    'message': metric.get_raw_payload_var('status'),
                    'type': "astats"
                }
                metric.set_metric_var('error', error_struct)
            new_metrics.append(metric)
        pipeline_context.add_var('metrics_list', new_metrics)