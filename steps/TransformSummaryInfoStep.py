from etl.PipelineStep import PipelineStep


class TransformSummaryInfoStep(PipelineStep):
    def __init__(self):
        super().__init__(self.__class__.__name__, dependencies=['metrics_list'])

    def run_step(self, pipeline_context):
        new_metrics = []
        for metric in pipeline_context.get_var('metrics_list'):
            is_up = metric.get_raw_payload_var('combined_available')
            summary_stats = {
                'up': float(2 if is_up else 0),
                'down': float(0 if is_up else 2),
            }
            metric.set_metric_var('summary', summary_stats)
            new_metrics.append(metric)
        pipeline_context.add_var('metrics_list', new_metrics)