from traffic_ops.ToWrapperInterface import ToWrapperInterface

__all__ = ['MockToWrapper']

class MockToWrapper(ToWrapperInterface):
    def __init__(self):
        pass

    def get_traffic_monitors(self) -> str:
        """Returns a pre-defined list of TrafficMonitorServer instances"""
        return ""
