class CacheGroupDTO:
    def __init__(self, apiData):
        self.__name = apiData['name']
        self.coords_lat = apiData['coordinates']['latitude']
        self.coords_long = apiData['coordinates']['longitude']

    def getName(self):
        return self.__name

    def getCoords(self):
        return [self.coords_lat, self.coords_long]
