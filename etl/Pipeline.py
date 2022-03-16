import logging
import time

from etl import PipelineStep
from etl.PipelineContext import PipelineContext
from util.APMWrapper import APMWrapper


class Pipeline:
    def __init__(self):
        self.__steps = []
        self.__metrics = APMWrapper()

    def add_step(self, step: PipelineStep, load_step=False):
        # Schedule step for execution in the proper order
        # Start by placing this step at the end of the list
        self.__steps.append(step)
        # Then recalculate the order of the steps
        if not load_step:
            self.recalculate_dependency_order(step)

    def run(self):
        # Start benchmarking data
        self.__metrics.start_transaction()
        pipeline_failed = False
        pipe_bench_start = time.perf_counter()
        # Create pipeline context
        context = PipelineContext()
        for step in self.__steps:
            try:
                step.run(context)
            except Exception as e:
                logging.error("Error running step {}: {}".format(step.get_name(), e))
                pipeline_failed = True
                break
        pipe_bench_end = time.perf_counter()
        logging.info(f"Pipeline took {(pipe_bench_end - pipe_bench_start) * 1000} ms.")
        self.__metrics.end_transaction('pipeline', 'success' if not pipeline_failed else 'failure')

    def recalculate_dependency_order(self, step: PipelineStep):
        dep_steps = [s for s in self.__steps if self.has_dependency(step, s)]
        for dep_step in dep_steps:
            if self.__steps.index(dep_step) < self.__steps.index(step):
                self.__steps.append(self.__steps.pop(self.__steps.index(dep_step)))
            else:
                dep_steps.remove(dep_step)
        for dep_step in dep_steps:
            self.recalculate_dependency_order(dep_step)

    def has_dependency(self, step: PipelineStep, dependency: PipelineStep):
        return (set(step.get_provides()) & set(dependency.get_dependencies())) != set()
