class MetricsDTO:
    def __init__(self, name: str, data: dict):
        self.__data = dict()
        self.__data['hostname'] = name
        self.__data['query_time_ms'] = data['query_time_ms']

    def get_data_dict(self) -> dict:
        return self.__data # TODO: Convert to histogram object or whatever Elastic wants

    def __str__(self):
        return str(self.__data)

    def __repr__(self):
        return str(self.__data)
