from typing import Tuple, List, Dict, Any, _SpecialForm

from traffic_ops.ToWrapperInterface import ToWrapperInterface
from trafficops import TOSession
from traffic_ops.TrafficMonitorDTO import TrafficMonitorDTO
from traffic_ops.TrafficServerDTO import TrafficServerDTO
from traffic_ops.CacheGroupDTO import CacheGroupDTO
import sys
import logging

__all__ = ['ToWrapper']


class ToWrapper(ToWrapperInterface):
    def __init__(self, host: str, port: int, user: str, password: str):
        self._session = TOSession(host_ip=host, host_port=port)
        self._session.login(user, password)
        logging.info("Authenticated successfully with Traffic Ops")

    def get_trafficops_data(self) -> tuple[
        list[TrafficMonitorDTO], dict[Any, CacheGroupDTO]]:
        """Gets a list of Traffric Monitor instances from Traffic Ops."""
        traffic_monitors = []
        cachegroupMappings = {}
        for cdn in self.__get_cdns():
            if cdn['name'] == 'ALL':
                continue
            logging.debug("Getting CDN details for %s", cdn['name'])
            cdn_details = self.__get_cdn_details(cdn['name'])
            for traffic_monitor in cdn_details['trafficMonitors']:
                traffic_monitors.append(TrafficMonitorDTO(traffic_monitor))
                logging.debug("Added Traffic Monitor %s", traffic_monitor['hostname'])
            for cachegroup in cdn_details['cacheGroups']:
                cachegroupMappings[cachegroup['name']] = CacheGroupDTO(cachegroup)
                logging.debug("Added Cachegroup %s", cachegroup['name'])
        return traffic_monitors, cachegroupMappings

    def __get_cdns(self):
        """Gets a list of CDNs from Traffic Ops."""
        cdns = self._session.get_cdns()
        return cdns[0]

    def __get_cdn_details(self, cdn_name: str) -> dict:
        """Gets a list of CDN details from Traffic Ops."""
        cdn_details = self._session.get_cdn_monitoring_info(cdn_name=cdn_name)
        return cdn_details[0]


if __name__ == '__main__':
    wrapper = ToWrapper(host=sys.argv[1], port=443, user=sys.argv[2], password=sys.argv[3])
    print(wrapper.get_traffic_monitors())
