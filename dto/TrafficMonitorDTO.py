class TrafficMonitorDTO:
    def __init__(self, payload, cdn_name):
        self.__fqdn = payload['fqdn']
        self.__cache_group = payload['cachegroup']
        self.__cdn_name = cdn_name

    def get_fqdn(self):
        return self.__fqdn

    def get_cache_group_name(self):
        return self.__cache_group

    def get_cdn_name(self):
        return self.__cdn_name
