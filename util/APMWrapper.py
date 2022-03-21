import logging
import os

import elasticapm
from elasticapm.conf.constants import OUTCOME


class APMWrapper:
    def __init__(self):
        if self.apm_enabled():
            self.__client = elasticapm.Client(service_name='ams', server_url=os.environ['ES_APM_URL'],
                                              secret_token=os.environ['ES_APM_SECRET'])
            elasticapm.instrument()
            logging.debug('APM enabled')
        else:
            logging.debug('APM is disabled, skipping APM initialization')

    def start_transaction(self):
        if self.apm_enabled():
            self.__client.begin_transaction(transaction_type='script')
            logging.debug('Started tracable APM transaction')

    def end_transaction(self, transaction_name: str, transaction_succeeded: bool):
        if self.apm_enabled():
            if transaction_succeeded:
                elasticapm.set_transaction_outcome(OUTCOME.SUCCESS)
                self.__client.end_transaction(transaction_name, 'success')
            else:
                elasticapm.set_transaction_outcome(OUTCOME.FAILURE)
                self.__client.end_transaction(transaction_name, 'failure')
            logging.debug('Ended tracable APM transaction')

    @staticmethod
    def apm_enabled():
        try:
            return os.environ['ES_APM_ENABLED'] == 'true'
        except KeyError:
            return False

    def capture_exception(self, e: Exception):
        self.__client.capture_exception(exc_info=(type(e), e, e.__traceback__), handled=True)
