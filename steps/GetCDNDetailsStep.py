from etl.PipelineStep import PipelineStep
from dto.CDNDetailsDTO import CDNDetailsDTO


class GetCDNDetailsStep(PipelineStep):
    def __init__(self):
        super().__init__(self.__class__.__name__, dependencies=['to_connection_info', 'cdn_list'], provides=['cdn_detail_list'])

    def run_step(self, pipeline_context):
        to_context = pipeline_context.get_var('to_connection_info').get_session()
        cdn_detail_list = {}
        for cdn in pipeline_context.get_var('cdn_list'):
            if cdn['name'] == 'ALL':  # Probing details of the ALL CDN apparently causes a lot of issues.
                continue
            cdn_detail_list[cdn['name']] = CDNDetailsDTO(to_context.get_cdn_monitoring_info(cdn_name=cdn['name'])[0], cdn['name'])
        pipeline_context.add_var('cdn_detail_list', cdn_detail_list)