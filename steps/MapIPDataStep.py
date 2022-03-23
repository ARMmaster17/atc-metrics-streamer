from watergrid.context import DataContext
from watergrid.steps import Step


class MapIPDataStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__, requires=['metrics_list', 'tm_list', 'cdn_detail_list'])

    def run(self, pipeline_context: DataContext):
        new_metrics = []
        for metric in pipeline_context.get('metrics_list'):
            # Get TM data
            tm_name = metric.get_traffic_monitor_name()
            tm_obj = pipeline_context.get('tm_list')[tm_name]
            cdn_name = tm_obj.get_cdn_name()
            cdn = pipeline_context.get('cdn_detail_list')[cdn_name]
            interfaces = cdn.get_traffic_server(metric.get_metric_var('hostname'))['interfaces']
            if len(interfaces) > 0:
                addresses = interfaces[0]['ipAddresses']
                if len(addresses) > 0:
                    address = addresses[0]['address']
                    if '/' in address:
                        address = address.split('/')[0]
                    metric.set_metric_var('ip_address', address)
            new_metrics.append(metric)
        pipeline_context.set('metrics_list', new_metrics)