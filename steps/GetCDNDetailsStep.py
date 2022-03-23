from watergrid.context import DataContext
from watergrid.steps import Step

from dto.CDNDetailsDTO import CDNDetailsDTO


class GetCDNDetailsStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__, requires=['to_connection_info', 'cdn_list'], provides=['cdn_detail_list'])

    def run(self, pipeline_context: DataContext):
        to_context = pipeline_context.get('to_connection_info').get_session()
        cdn_detail_list = {}
        for cdn in pipeline_context.get('cdn_list'):
            if cdn['name'] == 'ALL':  # Probing details of the ALL CDN apparently causes a lot of issues.
                continue
            cdn_detail_list[cdn['name']] = CDNDetailsDTO(to_context.get_cdn_monitoring_info(cdn_name=cdn['name'])[0], cdn['name'])
        pipeline_context.set('cdn_detail_list', cdn_detail_list)