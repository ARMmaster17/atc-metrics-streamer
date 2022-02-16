class TrafficServerDTO:
    def __init__(self, apiData):
        self.__hostname = apiData['name']
        self.__cachegroup = apiData['cachegroup']

    def getHostname(self) -> str:
        return self.__hostname

    def getCacheGroup(self) -> str:
        return self.__cachegroup