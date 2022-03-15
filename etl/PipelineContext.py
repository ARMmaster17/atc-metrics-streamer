class PipelineContext:
    def __init__(self):
        self.__vars = {}

    def add_var(self, key: str, value):
        self.__vars[key] = value

    def get_var(self, key: str):
        return self.__vars.get(key)