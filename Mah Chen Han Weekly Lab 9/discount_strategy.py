from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Strategy interface: every discount offers the same apply() method."""

    @abstractmethod
    def apply(self, total: float) -> float:
        """Takes an order total and returns the discounted total."""
        pass
