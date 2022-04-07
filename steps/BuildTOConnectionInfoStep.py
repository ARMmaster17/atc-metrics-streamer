import functools
import logging
import os

from trafficops import TOSession
from watergrid.context import DataContext
from watergrid.steps import Step

from dto.TOSessionDTO import TOSessionDTO


class BuildTOConnectionInfoStep(Step):
    def __init__(self, skip_connection=False):
        super().__init__(self.__class__.__name__, provides=['to_connection_info'])
        if skip_connection:
            return
        logging.info(f"Authenticating with Traffic Ops server {os.environ['TO_SERVER']}")
        self.__session = TOSession(host_ip=os.environ['TO_SERVER'], host_port=443)
        self.__session.login(os.environ['TO_USER'], os.environ['TO_PASSWORD'])

    def run(self, pipeline_context: DataContext):
        if not self.__session:
            pipeline_context.set('to_connection')
        pipeline_context.set('to_connection_info', TOSessionDTO(self.__session))
