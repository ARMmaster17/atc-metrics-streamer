from dto.TrafficMonitorDTO import TrafficMonitorDTO
from etl.PipelineStep import PipelineStep


class BuildTMListStep(PipelineStep):
    def __init__(self):
        super().__init__(self.__class__.__name__, dependencies=['cdn_detail_list'], provides=['tm_list'])

    def run_step(self, pipeline_context):
        traffic_monitors = {}
        for cdn in pipeline_context.get_var('cdn_detail_list'):
            for traffic_monitor in pipeline_context.get_var('cdn_detail_list')[cdn].get_traffic_monitors():
                traffic_monitors[traffic_monitor['hostname']] = TrafficMonitorDTO(traffic_monitor, cdn)
        pipeline_context.add_var('tm_list', traffic_monitors)
