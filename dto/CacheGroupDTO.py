class CacheGroupDTO:
    def __init__(self, payload):
        self.coords_lat = payload['coordinates']['latitude']
        self.coords_long = payload['coordinates']['longitude']
        self.__name = payload['name']

    def get_coordinates(self):
        return [self.coords_long, self.coords_lat]

    def get_name(self):
        return self.__name