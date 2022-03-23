from watergrid.context import DataContext
from watergrid.steps import Step


class DebugStep(Step):
    def __init__(self, var_name, is_list=False):
        super().__init__(self.__class__.__name__, requires=[var_name])
        self.__var_name = var_name
        self.__is_list = is_list

    def run(self, pipeline_context: DataContext):
        if self.__is_list:
            var_index = 0
            for var in pipeline_context.get(self.__var_name):
                print(f"{self.__var_name}[{var_index}] = {pipeline_context.get(self.__var_name)[var_index]}\n")
                var_index += 1
        else:
            print(f"{self.__var_name} = {pipeline_context.get(self.__var_name)}\n")