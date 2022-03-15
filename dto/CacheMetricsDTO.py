class CacheMetricsDTO:
    def __init__(self, payload, cache_group_name, traffic_monitor_name):
        self.__raw_payload = payload
        self.__metric_export = {}
        self.__cache_group_name = cache_group_name
        self.__traffic_monitor_name = traffic_monitor_name


    def get_raw_payload(self):
        return self.__raw_payload

    def get_raw_payload_var(self, var):
        return self.__raw_payload[var]

    def set_metric_var(self, var, value):
        self.__metric_export[var] = value

    def get_traffic_monitor_name(self) -> str:
        return self.__traffic_monitor_name

    # Used for testing only.
    def get_metric_var(self, var):
        return self.__metric_export[var]

    def get_metric_export(self):
        return self.__metric_export

    def __str__(self):
        return str(self.__metric_export)