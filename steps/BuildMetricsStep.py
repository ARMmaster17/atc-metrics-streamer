import requests

from dto.CacheMetricsDTO import CacheMetricsDTO
from etl.PipelineStep import PipelineStep


class BuildMetricsStep(PipelineStep):
    def __init__(self):
        super().__init__(self.__class__.__name__, dependencies=['tm_list'], provides=['metrics_list'])

    def run_step(self, pipeline_context):
        metrics = []
        for traffic_monitor in pipeline_context.get_var('tm_list'): # TODO: Move some of this to separate methods
            tm_url = 'http://{}/api/cache-statuses'.format(pipeline_context.get_var('tm_list')[traffic_monitor].get_fqdn())
            query_result = requests.get(tm_url, timeout=5)
            if query_result.status_code != 200:
                raise Exception('Failed to query TM {}: result code {}'.format(tm_url, query_result.status_code))
            for cache_status in query_result.json():
                new_metric = CacheMetricsDTO(query_result.json()[cache_status], None, traffic_monitor)
                new_metric.set_metric_var('hostname', cache_status)
                metrics.append(new_metric)
        pipeline_context.add_var('metrics_list', metrics)


