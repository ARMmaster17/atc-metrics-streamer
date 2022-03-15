import logging
from datetime import datetime, timezone, timedelta

import schedule

from etl.Pipeline import Pipeline
from steps.BuildCDNListStep import BuildCDNListStep
from steps.BuildCacheGroupListStep import BuildCacheGroupListStep
from steps.BuildMetricsStep import BuildMetricsStep
from steps.BuildObserverDataStep import BuildObserverDataStep
from steps.BuildTMListStep import BuildTMListStep
from steps.BuildTOConnectionInfoStep import BuildTOConnectionInfoStep
from steps.GetCDNDetailsStep import GetCDNDetailsStep
from steps.LoadIntoKafkaStep import LoadIntoKafkaStep
from steps.SetMetricStep import SetMetricStep
from steps.StepBuilder import StepBuilder


class Service:
    def __init__(self):
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        logging.info("Initializing pipeline")
        # Initialize all steps of the pipeline
        self.__pipeline = Pipeline()
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
        self.__pipeline.add_step(SetMetricStep('check_time', datetime.now(timezone.utc).isoformat()))
        self.__pipeline.add_step(SetMetricStep('next_check', (datetime.now(timezone.utc) + timedelta(seconds=10)).isoformat()))
        self.__pipeline.add_step(BuildObserverDataStep())
        self.__pipeline.add_step(LoadIntoKafkaStep(), load_step=True)
        logging.info("Scheduling pipeline")
        schedule.every(10).seconds.do(self.run)

    def start(self):
        logging.info("Starting pipeline")
        while True:
            schedule.run_pending()

    def run(self):
        self.__pipeline.run()