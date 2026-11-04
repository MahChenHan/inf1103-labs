import json
import os

FILENAME = "inventory.json"


# ============================================================================
# BASE CLASS (Parent)
# ============================================================================
class Product:
    """Base Product class containing common product attributes and methods."""

    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self._product_id = str(product_id)
        self.name = name
        self._price = float(price)
        self._stock = int(stock)

    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def price(self) -> float:
        return self._price

    @property
    def stock(self) -> int:
        return self._stock

    def update_stock(self, new_stock: int) -> None:
        """Updates internal stock quantity with validation."""
        if new_stock < 0:
            raise ValueError("Stock quantity cannot be negative!")
        self._stock = int(new_stock)

    def display_information(self) -> None:
        """Base implementation: Displays common product details."""
        print("-" * 45)
        print(f"ID: {self._product_id}")
        print(f"Name: {self.name}")
        print(f"Price: ${self._price:.2f}")
        print(f"Stock: {self._stock}")


# ============================================================================
# PHYSICAL PRODUCT SUBCLASS (Child)
# ============================================================================
class PhysicalProduct(Product):
    """Represents a physical product with a weight attribute."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float):
        super().__init__(product_id, name, price, stock)
        self._weight = float(weight)

    @property
    def weight(self) -> float:
        return self._weight

    def display_information(self) -> None:
        """
        Section 2.1 Overriding:
        Reuses base implementation via super(), then appends weight.
        """
        super().display_information()  # Call parent display_information()
        print(f"Weight: {self._weight:.2f} kg")
        print("-" * 45)


# ============================================================================
# DIGITAL PRODUCT SUBCLASS (Child)
# ============================================================================
class DigitalProduct(Product):
    """Represents a digital product with a download_size attribute."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float):
        super().__init__(product_id, name, price, stock)
        self._download_size = float(download_size)

    @property
    def download_size(self) -> float:
        return self._download_size

    def display_information(self) -> None:
        """
        Section 2.1 Overriding:
        Reuses base implementation via super(), then appends download size.
        """
        super().display_information()  # Call parent display_information()
        print(f"Download Size: {self._download_size:.2f} MB")
        print("-" * 45)


# ============================================================================
# SECTION 2.2 TESTING
# ============================================================================
if __name__ == "__main__":
    print("=== Testing Section 2: Method Overriding ===")
    
    # 1. Create one physical product and one digital product
    physical_item = PhysicalProduct("P101", "Mechanical Keyboard", 129.99, 15, 1.20)
    digital_item = DigitalProduct("D101", "Python Programming eBook", 19.99, 50, 15.40)

    # 2. Call display_information() on each to verify combined output
    print("\n[Physical Product Details]")
    physical_item.display_information()

    print("\n[Digital Product Details]")
    digital_item.display_information()