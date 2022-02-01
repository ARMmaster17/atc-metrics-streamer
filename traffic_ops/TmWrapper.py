from traffic_ops import TrafficMonitorDTO
import requests

from traffic_ops.MetricsDTO import MetricsDTO


class TmWrapper:
    def __init__(self):
        pass

    def get_tm_metrics(self, tm_instance: TrafficMonitorDTO, metric_mappings: list) -> dict:
        tm_url = 'http://{}/api/cache-statuses'.format(tm_instance.get_fqdn())
        result = requests.get(tm_url)
        results = []
        if result.status_code != 200:
            raise Exception('Error getting cache status from Traffic Monitor: {}'.format(result.status_code))
        for cache_status in result.json():
            results.append(MetricsDTO(cache_status, result.json()[cache_status], metric_mappings))
        return results

