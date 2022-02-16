__all__ = ['ToWrapperInterface']

from typing import Any

from traffic_ops.TrafficMonitorDTO import TrafficMonitorDTO
from traffic_ops.TrafficServerDTO import TrafficServerDTO
from traffic_ops.CacheGroupDTO import CacheGroupDTO


class ToWrapperInterface:
    """Base class for Traffic Ops wrapper class. Allows mocking of TO endpoints for local development and testing."""

    def get_trafficops_data(self) -> tuple[
        list[TrafficMonitorDTO], dict[Any, CacheGroupDTO]]:
        """Returns all traffic monitors associated with this Traffic Ops instance."""
        pass
