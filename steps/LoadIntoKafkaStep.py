import json
import os

from kafka import KafkaProducer

from etl.PipelineStep import PipelineStep


class LoadIntoKafkaStep(PipelineStep):
    def __init__(self):
        super().__init__(self.__class__.__name__, dependencies=['metrics_list'])
        self.__kakfa_producer = KafkaProducer(bootstrap_servers=os.environ['KAFKA_SERVERS'])

    def run_step(self, pipeline_context):
        for metric in pipeline_context.get_var('metrics_list'):
            self.__kakfa_producer.send(os.environ['KAFKA_TOPIC'], bytes(json.dumps(metric.get_metric_export()), encoding='utf-8'))
