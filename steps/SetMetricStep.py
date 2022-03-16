from etl.PipelineStep import PipelineStep


class SetMetricStep(PipelineStep):
    def __init__(self, key, value):
        super().__init__("Set-{}".format(key), dependencies=['metrics_list'])
        self.__key = key
        self.__value = value

    def run_step(self, pipeline_context):
        new_metrics = []
        for metric in pipeline_context.get_var('metrics_list'):
            metric.set_metric_var(self.__key, self.__value)
            new_metrics.append(metric)
        pipeline_context.add_var('metrics_list', new_metrics)