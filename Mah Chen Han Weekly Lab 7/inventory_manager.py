from abc import ABC, abstractmethod
import json
import os

FILENAME = "inventory.json"


# ============================================================================
# 4.1 CAN BE SHIPPED INTERFACE (Section 4.1)
# ============================================================================
class CanBeShipped(ABC):
    """
    Interface specifying the shipping cost capability.
    Classes implementing this contract must provide calculate_shipping_cost().
    """

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Calculates and returns shipping cost based on product properties."""
        pass


# ============================================================================
# 3.1 ABSTRACT BASE CLASS (Section 3.1)
# ============================================================================
class Product(ABC):
    """
    Abstract base class for all products in the system.
    Cannot be instantiated directly.
    """

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

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Abstract method enforcing fulfilment implementation in subclasses."""
        pass


# ============================================================================
# 4.2 PHYSICAL PRODUCT SUBCLASS (Inherits Product, Realises CanBeShipped)
# ============================================================================
class PhysicalProduct(Product, CanBeShipped):
    """
    Represents a physical product requiring physical shipping.
    Implements CanBeShipped interface.
    """

    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float):
        super().__init__(product_id, name, price, stock)
        self._weight = float(weight)

    @property
    def weight(self) -> float:
        return self._weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self._weight:.2f} kg")
        print(f"Fulfilment: {self.get_fulfilment_info()}")
        # Display shipping cost calculated via CanBeShipped interface
        print(f"Est. Shipping Cost: ${self.calculate_shipping_cost():.2f}")
        print("-" * 45)

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping."

    # Section 4.2: Interface implementation
    def calculate_shipping_cost(self) -> float:
        """Calculates shipping cost based on product weight ($5.00 base + $2.50 per kg)."""
        return 5.00 + (self._weight * 2.50)


# ============================================================================
# 3.2 DIGITAL PRODUCT SUBCLASS (Does NOT implement CanBeShipped)
# ============================================================================
class DigitalProduct(Product):
    """
    Represents a digital product delivered online.
    Does not implement CanBeShipped interface.
    """

    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float):
        super().__init__(product_id, name, price, stock)
        self._download_size = float(download_size)

    @property
    def download_size(self) -> float:
        return self._download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self._download_size:.2f} MB")
        print(f"Fulfilment: {self.get_fulfilment_info()}")
        print("-" * 45)

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally via download link."


# ============================================================================
# SECTION 4 TESTING
# ============================================================================
if __name__ == "__main__":
    print("=== Testing Section 4: Interface Realisation ===")

    # Create physical products with different weights
    light_item = PhysicalProduct("P101", "USB Cable", 9.99, 50, 0.10)
    heavy_item = PhysicalProduct("P102", "Desktop Computer", 1499.00, 5, 8.50)

    # Create a digital product
    digital_item = DigitalProduct("D101", "Design Software", 99.99, 100, 1200.0)

    print("\n[Light Physical Product]")
    light_item.display_information()

    print("\n[Heavy Physical Product]")
    heavy_item.display_information()

    print("\n[Digital Product - No Shipping]")
    digital_item.display_information()