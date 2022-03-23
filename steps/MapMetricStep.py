from watergrid.context import DataContext
from watergrid.steps import Step


class MapMetricStep(Step):
    def __init__(self, source, dest):
        super().__init__("Map-{}-{}".format(source, dest), requires=['metrics_list'])
        self.__source = source
        self.__dest = dest

    def run(self, pipeline_context: DataContext):
        new_metrics = []
        for metric in pipeline_context.get('metrics_list'):
            copy_metric = metric.get_raw_payload_var(self.__source)
            metric.set_metric_var(self.__dest, copy_metric)
            new_metrics.append(metric)
        pipeline_context.set('metrics_list', new_metrics)