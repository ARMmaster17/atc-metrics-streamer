import logging
import time
from abc import abstractmethod, ABC


class PipelineStep(ABC):
    def __init__(self, name, dependencies=[], provides=[]):
        self.__name = name
        self.__dependencies = dependencies
        self.__provides = provides

    def get_name(self):
        return self.__name

    def get_dependencies(self):
        return self.__dependencies

    def get_provides(self):
        return self.__provides

    def run(self, pipeline_context):
        bench_start = time.perf_counter()
        self.run_step(pipeline_context)
        bench_end = time.perf_counter()
        logging.info("Step {} took {} ms".format(self.get_name(), (bench_end - bench_start) * 1000))

    @abstractmethod
    def run_step(self, pipeline_context):
        pass
