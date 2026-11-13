from discount_strategy import DiscountStrategy


class BulkDiscount(DiscountStrategy):
    """Takes a fixed amount off when the total reaches a threshold,
    e.g. BulkDiscount(200, 20) = $20 off any total of $200 or more."""

    def __init__(self, threshold: float, amount: float):
        self.threshold: float = threshold
        self.amount: float = amount

    def apply(self, total: float) -> float:
        return total - self.amount if total >= self.threshold else total
