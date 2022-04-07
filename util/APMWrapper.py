import logging
import os

import elasticapm
from elasticapm import Client, instrument
from elasticapm.conf.constants import OUTCOME
from watergrid.metrics.MetricsExporter import MetricsExporter


class ElasticAPMMetricsExporter(MetricsExporter):
    def __init__(self):
        super().__init__()
        self.__client = Client(service_name='ams', server_url=os.environ['ES_APM_URL'],
                               secret_token=os.environ['ES_APM_SECRET'])
        instrument()
        self.__pipeline_failed = False
        self.__pipeline_name = None

    def start_pipeline(self, pipeline_name: str):
        self.__client.begin_transaction(transaction_type='script')
        self.__pipeline_name = pipeline_name

    def end_pipeline(self):
        if self.__pipeline_failed:
            elasticapm.set_transaction_outcome(OUTCOME.FAILURE)
            self.__client.end_transaction(self.__pipeline_name, 'failure')
            self.__pipeline_failed = False
        else:
            elasticapm.set_transaction_outcome(OUTCOME.SUCCESS)
            self.__client.end_transaction(self.__pipeline_name, 'success')

    def start_step(self, step_name: str):
        pass  # This is handled by the instrumentation functions of Elastic APM.

    def end_step(self):
        pass  # This is handled by the instrumentation functions of Elastic APM.

    def capture_exception(self, e: Exception):
        self.__client.capture_exception(exc_info=(type(e), e, e.__traceback__), handled=True)
        self.__pipeline_failed = True
