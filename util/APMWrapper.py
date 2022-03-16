import logging
import os

import elasticapm


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

    def end_transaction(self, transaction_name: str, transaction_result: str):
        if self.apm_enabled():
            self.__client.end_transaction(name=transaction_name, result=transaction_result)
            logging.debug('Ended tracable APM transaction')

    def apm_enabled(self):
        try:
            return os.environ['ES_APM_ENABLED'] == 'true'
        except KeyError:
            return False
