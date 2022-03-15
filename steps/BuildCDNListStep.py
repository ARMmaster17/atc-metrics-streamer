from etl.PipelineStep import PipelineStep

class BuildCDNListStep(PipelineStep):
    def __init__(self):
        super().__init__(self.__class__.__name__, dependencies=['to_connection_info'], provides=['cdn_list'])

    def run_step(self, pipeline_context):
        to_context = pipeline_context.get_var('to_connection_info').get_session()
        pipeline_context.add_var('cdn_list', to_context.get_cdns()[0])
