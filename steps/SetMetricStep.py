from watergrid.context import DataContext
from watergrid.steps import Step


class SetMetricStep(Step):
    def __init__(self, key, value):
        super().__init__("Set-{}".format(key), requires=['metrics_list'])
        self.__key = key
        self.__value = value

    def run(self, pipeline_context: DataContext):
        new_metrics = []
        for metric in pipeline_context.get('metrics_list'):
            metric.set_metric_var(self.__key, self.__value)
            new_metrics.append(metric)
        pipeline_context.set('metrics_list', new_metrics)