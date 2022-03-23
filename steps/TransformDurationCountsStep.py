from watergrid.context import DataContext
from watergrid.steps import Step


class TransformDurationCountsStep(Step):
    def __init__(self, field_name: str):
        super().__init__(self.__class__.__name__, requires=['metrics_list'])
        self.__field_name = field_name

    def run(self, pipeline_context: DataContext):
        new_metrics = []
        for metric in pipeline_context.get('metrics_list'):
            field_value = metric.get_metric_var(self.__field_name)
            us_field_value = int(field_value) * 1000
            us_field_name = str.replace(self.__field_name, "_ms", "_us")
            metric.set_metric_var(us_field_name, us_field_value)
            new_metrics.append(metric)
        pipeline_context.set('metrics_list', new_metrics)