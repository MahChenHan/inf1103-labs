from discount_strategy import DiscountStrategy
from no_discount import NoDiscount
from order_line import OrderLine
from product import Product


class Order:
    """COMPOSITION: Order creates, owns and removes its OrderLine objects.
    ASSOCIATION: Order USES a DiscountStrategy but does not own it."""

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        self.discount: DiscountStrategy = discount if discount else NoDiscount()

    def set_discount(self, discount: DiscountStrategy) -> None:
        """Swap the discount strategy at any time."""
        self.discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)   # created INSIDE the Order
        self.order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for line in self.order_lines:
            if line.product.product_id == product_id:
                self.order_lines.remove(line)
                return True
        return False

    def calculate_subtotal(self) -> float:
        """Total before discount."""
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def calculate_total(self) -> float:
        """Total after discount. No if/elif: the strategy decides."""
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)

    def display_order(self) -> None:
        print(f"Order {self.order_id}")
        if not self.order_lines:
            print("  (no order lines)")
        for line in self.order_lines:
            line.display()
        print(f"  Subtotal: ${self.calculate_subtotal():.2f}")
        print(f"  Discount: {type(self.discount).__name__}")
        print(f"  TOTAL: ${self.calculate_total():.2f}")
