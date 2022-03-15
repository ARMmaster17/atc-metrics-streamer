from etl.PipelineStep import PipelineStep


class MapMetricStep(PipelineStep):
    def __init__(self, source, dest):
        super().__init__("Map-{}-{}".format(source, dest), dependencies=['metrics_list'])
        self.__source = source
        self.__dest = dest

    def run_step(self, pipeline_context):
        new_metrics = []
        for metric in pipeline_context.get_var('metrics_list'):
            copy_metric = metric.get_raw_payload_var(self.__source)
            metric.set_metric_var(self.__dest, copy_metric)
            new_metrics.append(metric)
        pipeline_context.add_var('metrics_list', new_metrics)