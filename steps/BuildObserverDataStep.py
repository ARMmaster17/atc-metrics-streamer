from watergrid.context import DataContext
from watergrid.steps import Step


class BuildObserverDataStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__, requires=['tm_list', 'cache_group_list', 'metrics_list'], provides=['metrics_list'])

    def run(self, pipeline_context: DataContext):
        new_metrics = []
        for metric in pipeline_context.get('metrics_list'):
            # Get TM data
            tm_name = metric.get_traffic_monitor_name()
            tm_obj = pipeline_context.get('tm_list')[tm_name]
            # Inject TM data into metric
            metric.set_metric_var('obv_name', tm_obj.get_fqdn())
            # Get cache group data
            cache_group_name = tm_obj.get_cache_group_name()
            cache_group_obj = pipeline_context.get('cache_group_list')[cache_group_name]
            # Inject cache group data into metric
            metric.set_metric_var('obv_coord', cache_group_obj.get_coordinates())
            metric.set_metric_var('obv_location', cache_group_obj.get_name())
            # Add new metric to replacement list
            new_metrics.append(metric)
        pipeline_context.set('metrics_list', new_metrics)