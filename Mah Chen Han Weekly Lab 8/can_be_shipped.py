from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface specifying shipping cost calculation contract."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Calculates and returns shipping cost based on product characteristics."""
        pass
