import os

from traffic_ops.ToWrapperInterface import ToWrapperInterface
from traffic_ops.ToWrapper import ToWrapper
from traffic_ops.TmWrapper import TmWrapper
import schedule
import time
import logging
import sys
import json
import yaml
import traceback
from kafka import KafkaProducer


class BaseService:
    def __init__(self, to_wrapper: ToWrapperInterface, tm_wrapper: TmWrapper, log_level: int = logging.DEBUG):
        logging.basicConfig(level=log_level)
        self.__to_service = to_wrapper
        self.__tm_wrapper = tm_wrapper
        self.__tm_list = None
        self.__cg_dict = None
        self.__kafka_producer = KafkaProducer(bootstrap_servers=os.environ['KAFKA_SERVERS'])
        with open('/opt/mappings.yaml', 'r') as f:
            self.__metric_mappings = yaml.load(f, Loader=yaml.FullLoader)
        schedule.every(60).seconds.do(self.__update_to_service_list)
        schedule.every(10).seconds.do(self.__publish_metrics)

    def start(self):
        logging.info("Starting service")
        while True:
            logging.debug("Scheduler tick")
            schedule.run_pending()
            time.sleep(1)

    def __update_to_service_list(self):
        logging.debug("Updating Traffic Ops list")
        self.__tm_list, self.__cg_dict = self.__to_service.get_trafficops_data()

    def __publish_metrics(self):
        logging.debug("Publishing metrics")
        if self.__tm_list is None:
            logging.warning("No Traffic Monitors available, skipping metrics publish step")
            return
        checked_hostnames = []
        for tm in self.__tm_list:
            try:
                metrics = self.__tm_wrapper.get_tm_metrics(tm, self.__metric_mappings, checked_hostnames, self.__cg_dict[tm.get_cachegroup()])
                for metric in metrics:
                    self.__kafka_producer.send(os.environ['KAFKA_TOPIC'], bytes(json.dumps(metric.get_data_dict()), encoding='utf-8'))
            except Exception as e:
                logging.warning("Error publishing metrics for Traffic Monitor %s: %s (skipping)", tm.get_fqdn(), e)
                # TODO: Remove this
                traceback.print_exception(type(e), e, e.__traceback__)


if __name__ == '__main__':
    wrapper = ToWrapper(host=sys.argv[1], port=443, user=sys.argv[2], password=sys.argv[3])
    svc = BaseService(wrapper, TmWrapper())
    svc.start()
