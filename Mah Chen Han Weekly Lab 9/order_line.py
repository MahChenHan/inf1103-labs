from product import Product


class OrderLine:
    """One product + quantity inside an Order. Only Order should create these."""

    def __init__(self, product: Product, quantity: int):
        # VALIDATION: OrderLine protects its own quantity
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.product: Product = product   # association: refers to, not owns
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

    def display(self) -> None:
        print(f"  {self.product.name} x {self.quantity} "
              f"@ ${self.product.price:.2f} = ${self.calculate_subtotal():.2f}")
