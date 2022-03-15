class CDNDetailsDTO:
    def __init__(self, payload):
        self.__traffic_monitors = payload['trafficMonitors']
        self.__cache_groups = payload['cacheGroups']

    def get_traffic_monitors(self):
        return self.__traffic_monitors

    def get_cache_groups(self):
        return self.__cache_groups

