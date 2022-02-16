from typing import List

from traffic_ops import TrafficMonitorDTO
import requests

from traffic_ops.MetricsDTO import MetricsDTO


class TmWrapper:
    def __init__(self):
        pass

    def get_tm_metrics(self, tm_instance: TrafficMonitorDTO, metric_mappings: list, checked_hostnames: list, cacheGroupData) -> list[MetricsDTO]:
        tm_url = 'http://{}/api/cache-statuses'.format(tm_instance.get_fqdn())
        result = requests.get(tm_url, timeout=5)
        results = []
        if result.status_code != 200:
            raise Exception('Error getting cache status from Traffic Monitor: {}'.format(result.status_code))
        tmData = {
            'obv_name': tm_instance.get_fqdn(),
            'obv_coord': cacheGroupData.getCoords(),
            'obv_location': cacheGroupData.getName(),
        }
        for cache_status in result.json():
            newDTO = MetricsDTO(cache_status, result.json()[cache_status], metric_mappings, tmData)
            if newDTO.get_hostname() not in checked_hostnames:
                results.append(newDTO)
                checked_hostnames.append(newDTO.get_hostname())
        return results
