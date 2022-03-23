import json
import os

from kafka import KafkaProducer
from watergrid.context import DataContext
from watergrid.steps import Step


class LoadIntoKafkaStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__, requires=['metrics_list'])
        self.__kakfa_producer = KafkaProducer(bootstrap_servers=os.environ['KAFKA_SERVERS'])

    def run(self, pipeline_context: DataContext):
        for metric in pipeline_context.get('metrics_list'):
            self.__kakfa_producer.send(os.environ['KAFKA_TOPIC'], bytes(json.dumps(metric.get_metric_export()), encoding='utf-8'))
