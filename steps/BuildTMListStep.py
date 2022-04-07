from watergrid.context import DataContext
from watergrid.steps import Step

from dto.TrafficMonitorDTO import TrafficMonitorDTO


class BuildTMListStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__, requires=['cdn_detail_list'], provides=['tm_list'])

    def run(self, pipeline_context: DataContext):
        traffic_monitors = {}
        for cdn in pipeline_context.get('cdn_detail_list'):
            for traffic_monitor in pipeline_context.get('cdn_detail_list')[cdn].get_traffic_monitors():
                traffic_monitors[traffic_monitor['hostname']] = TrafficMonitorDTO(traffic_monitor, cdn)
        pipeline_context.set('tm_list', traffic_monitors)
