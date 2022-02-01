class MetricsDTO:
    def __init__(self, name: str, data: dict, mappings: list):
        self.__data = dict()
        data['hostname'] = name
        for mapping in mappings:
            self.__data[mapping['output']] = data[mapping['input']]

    def get_data_dict(self) -> dict:
        return self.__data

    def __str__(self):
        return str(self.__data)

    def __repr__(self):
        return str(self.__data)
