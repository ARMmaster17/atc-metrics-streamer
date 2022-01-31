__all__ = ['ToWrapperInterface']


class ToWrapperInterface:
    """Base class for Traffic Ops wrapper class. Allows mocking of TO endpoints for local development and testing."""

    def get_traffic_monitors(self) -> list:
        """Returns all traffic monitors associated with this Traffic Ops instance."""
        pass
