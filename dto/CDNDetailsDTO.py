class CDNDetailsDTO:
    def __init__(self, payload, cdn_name):
        self.__traffic_monitors = payload['trafficMonitors']
        self.__cache_groups = payload['cacheGroups']
        self.__traffic_servers = payload['trafficServers']
        self.__name = cdn_name

    def get_traffic_monitors(self):
        return self.__traffic_monitors

    def get_cache_groups(self):
        return self.__cache_groups

    def get_traffic_server(self, hostname):
        for ts in self.__traffic_servers:
            if ts['hostname'] == hostname:
                return ts

    def get_name(self):
        return self.__name

