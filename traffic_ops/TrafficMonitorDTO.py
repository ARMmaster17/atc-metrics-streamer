class TrafficMonitorDTO:
    def __init__(self, apiData):
        self.fqdn = apiData['fqdn']
        self.__cacheGroup = apiData['cachegroup']

    def get_fqdn(self):
        return self.fqdn

    def get_cachegroup(self):
        return self.__cacheGroup

    def __str__(self):
        return str(self.fqdn)
