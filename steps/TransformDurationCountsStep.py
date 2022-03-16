from etl.PipelineContext import PipelineContext
from etl.PipelineStep import PipelineStep


class TransformDurationCountsStep(PipelineStep):
    def __init__(self, field_name: str):
        super().__init__(self.__class__.__name__, dependencies=['metrics_list'])
        self.__field_name = field_name

    def run_step(self, pipeline_context: PipelineContext):
        new_metrics = []
        for metric in pipeline_context.get_var('metrics_list'):
            field_value = metric.get_metric_var(self.__field_name)
            us_field_value = int(field_value) * 1000
            us_field_name = str.replace(self.__field_name, "_ms", "_us")
            metric.set_metric_var(us_field_name, us_field_value)
            new_metrics.append(metric)
        pipeline_context.add_var('metrics_list', new_metrics)