from discount_strategy import DiscountStrategy


class NoDiscount(DiscountStrategy):
    """Default strategy: the total is returned unchanged."""

    def apply(self, total: float) -> float:
        return total
