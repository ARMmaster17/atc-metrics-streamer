from datetime import datetime, timezone, timedelta

class MetricsDTO:
    def __init__(self, name: str, data: dict, mappings: list):
        self.__data = dict()
        data['hostname'] = name
        data['check_time'] = datetime.now(timezone.utc).isoformat()
        data['next_check'] = (datetime.now(timezone.utc) + timedelta(seconds=10)).isoformat()
        for mapping in mappings:
            self.__data[mapping['output']] = data[mapping['input']]

    def get_data_dict(self) -> dict:
        return self.__data

    def __str__(self):
        return str(self.__data)

    def __repr__(self):
        return str(self.__data)
