from discount_strategy import DiscountStrategy


class StudentDiscount(DiscountStrategy):
    """Section 2.4: a new strategy added WITHOUT changing Order (OCP)."""

    STUDENT_RATE: float = 5.0   # 5% off for students

    def apply(self, total: float) -> float:
        return total * (1 - self.STUDENT_RATE / 100)
