from watergrid.context import DataContext
from watergrid.steps import Step


class BuildCDNListStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__, requires=['to_connection_info'], provides=['cdn_list'])

    def run(self, pipeline_context: DataContext):
        to_context = pipeline_context.get('to_connection_info').get_session()
        pipeline_context.set('cdn_list', to_context.get_cdns()[0])
