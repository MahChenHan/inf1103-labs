from order_line import OrderLine
from product import Product


class Order:
    """COMPOSITION: Order creates, owns and removes its OrderLine objects."""

    def __init__(self, order_id: str):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)   # created INSIDE the Order
        self.order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for line in self.order_lines:
            if line.product.product_id == product_id:
                self.order_lines.remove(line)
                return True
        return False

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_order(self) -> None:
        print(f"Order {self.order_id}")
        if not self.order_lines:
            print("  (no order lines)")
        for line in self.order_lines:
            line.display()
        print(f"  TOTAL: ${self.calculate_total():.2f}")
