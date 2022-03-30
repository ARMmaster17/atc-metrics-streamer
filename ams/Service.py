import logging
import os

from watergrid.locks import RedisPipelineLock
from watergrid.pipelines import HAPipeline

from steps.BuildCDNListStep import BuildCDNListStep
from steps.BuildCacheGroupListStep import BuildCacheGroupListStep
from steps.BuildMetricsStep import BuildMetricsStep
from steps.BuildObserverDataStep import BuildObserverDataStep
from steps.BuildTMListStep import BuildTMListStep
from steps.BuildTOConnectionInfoStep import BuildTOConnectionInfoStep
from steps.DebugStep import DebugStep
from steps.GetCDNDetailsStep import GetCDNDetailsStep
from steps.LoadIntoKafkaStep import LoadIntoKafkaStep
from steps.MapIPDataStep import MapIPDataStep
from steps.StepBuilder import StepBuilder
from steps.TransformDurationCountsStep import TransformDurationCountsStep
from steps.TransformErrorDataStep import TransformErrorDataStep
from steps.TransformSummaryInfoStep import TransformSummaryInfoStep
from steps.TransformTimestampsStep import TransformTimestampsStep
from util.APMWrapper import ElasticAPMMetricsExporter


class Service:
    def __init__(self):
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        logging.info("Initializing pipeline")
        # Setup global pipeline lock
        pipeline_lock = RedisPipelineLock(lock_timeout=5)
        pipeline_lock.set_host('redis')
        pipeline_lock.connect()
        # Initialize pipeline
        self.__pipeline = HAPipeline('ams-pipeline', pipeline_lock)
        # Set up pipeline configuration
        if self.apm_enabled():
            self.__pipeline.add_metrics_exporter(ElasticAPMMetricsExporter())
        # Set up pipeline steps
        self.__pipeline.add_step(BuildTOConnectionInfoStep())
        self.__pipeline.add_step(BuildCDNListStep())
        self.__pipeline.add_step(GetCDNDetailsStep())
        self.__pipeline.add_step(BuildTMListStep())
        self.__pipeline.add_step(BuildCacheGroupListStep())
        self.__pipeline.add_step(BuildMetricsStep())
        direct_map_vars = ['type', 'load_average', 'query_time_ms', 'health_time_ms', 'stat_time_ms',
                           'stat_span_ms', 'health_span_ms', 'bandwidth_kbps', 'bandwidth_capacity_kbps',
                           'connection_count', 'combined_available']
        for step in StepBuilder.build_multi_direct_map_steps(direct_map_vars):
            self.__pipeline.add_step(step)
        self.__pipeline.add_step(TransformDurationCountsStep('health_time_ms'))
        self.__pipeline.add_step(TransformDurationCountsStep('stat_time_ms'))
        self.__pipeline.add_step(TransformDurationCountsStep('query_time_ms'))
        self.__pipeline.add_step(TransformDurationCountsStep('stat_span_ms'))
        self.__pipeline.add_step(TransformDurationCountsStep('health_span_ms'))
        self.__pipeline.add_step(TransformTimestampsStep())
        self.__pipeline.add_step(BuildObserverDataStep())
        self.__pipeline.add_step(MapIPDataStep())
        self.__pipeline.add_step(TransformSummaryInfoStep())
        self.__pipeline.add_step(TransformErrorDataStep())
        self.__pipeline.add_step(DebugStep("metrics_list"))
        #self.__pipeline.add_step(LoadIntoKafkaStep())
        logging.info("Scheduling pipeline")
        self.__pipeline.run_interval(10)

    @staticmethod
    def apm_enabled():
        try:
            return os.environ['ES_APM_ENABLED'] == 'true'
        except KeyError:
            return False