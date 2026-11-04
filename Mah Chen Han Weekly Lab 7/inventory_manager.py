import json
import os

FILENAME = "inventory.json"


# ============================================================================
# BASE CLASS (Section 1.1)
# ============================================================================
class Product:
    """Base Product class containing common product details."""

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
        """Updates internal stock quantity with input validation."""
        if new_stock < 0:
            raise ValueError("Stock quantity cannot be negative!")
        self._stock = int(new_stock)

    def display_information(self) -> None:
        """Displays base product details."""
        print("-" * 45)
        print(f"ID: {self._product_id}")
        print(f"Name: {self.name}")
        print(f"Price: ${self._price:.2f}")
        print(f"Stock: {self._stock}")


# ============================================================================
# PHYSICAL PRODUCT SUBCLASS (Section 1.2)
# ============================================================================
class PhysicalProduct(Product):
    """
    Represents a physical item inheriting from Product.
    Introduces weight as a new attribute.
    """

    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float):
        super().__init__(product_id, name, price, stock)
        self._weight = float(weight)

    @property
    def weight(self) -> float:
        return self._weight

    def display_information(self) -> None:
        """Displays existing product information alongside its weight."""
        super().display_information()
        print(f"Weight: {self._weight:.2f} kg")
        print("-" * 45)


# ============================================================================
# DIGITAL PRODUCT SUBCLASS (Section 1.3)
# ============================================================================
class DigitalProduct(Product):
    """
    Represents a digital item inheriting from Product.
    Introduces download size as a new attribute.
    """

    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float):
        # Reuse existing Product constructor using super()
        super().__init__(product_id, name, price, stock)
        # Initialise additional download size attribute (in MB)
        self._download_size = float(download_size)

    @property
    def download_size(self) -> float:
        return self._download_size

    def display_information(self) -> None:
        """Displays existing product information alongside its download size."""
        super().display_information()
        print(f"Download Size: {self._download_size:.2f} MB")
        print("-" * 45)


# ============================================================================
# TEST EXECUTION FOR SECTION 1.2 & 1.3
# ============================================================================
if __name__ == "__main__":
    print("Testing PhysicalProduct Creation:")
    physical_item = PhysicalProduct("P001", "Gaming Mouse", 59.99, 20, 0.25)
    physical_item.display_information()

    print("\nTesting DigitalProduct Creation:")
    digital_item = DigitalProduct("D001", "Antivirus Software", 29.99, 100, 450.50)
    digital_item.display_information()