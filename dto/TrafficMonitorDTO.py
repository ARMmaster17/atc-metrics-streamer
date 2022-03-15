class TrafficMonitorDTO:
    def __init__(self, payload):
        self.__fqdn = payload['fqdn']
        self.__cache_group = payload['cachegroup']

    def get_fqdn(self):
        return self.__fqdn

    def get_cache_group_name(self):
        return self.__cache_group
