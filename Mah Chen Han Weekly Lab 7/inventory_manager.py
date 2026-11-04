from abc import ABC, abstractmethod
import json
import os

FILENAME = "inventory.json"


# ============================================================================
# 3.1 ABSTRACT BASE CLASS (Section 3.1)
# ============================================================================
class Product(ABC):
    """
    Abstract base class for all products in the system.
    Cannot be instantiated directly due to abstract methods.
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

    # Abstract Method (Section 3.1)
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """
        Abstract method enforcing concrete fulfilment implementation in subclasses.
        Does not provide an implementation in the base class.
        """
        pass


# ============================================================================
# 3.2 PHYSICAL PRODUCT CONCRETE SUBCLASS
# ============================================================================
class PhysicalProduct(Product):
    """Represents a physical product requiring physical shipping."""

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
        print("-" * 45)

    # Implements abstract method (Section 3.2)
    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping."


# ============================================================================
# 3.2 DIGITAL PRODUCT CONCRETE SUBCLASS
# ============================================================================
class DigitalProduct(Product):
    """Represents a digital product delivered online."""

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

    # Implements abstract method (Section 3.2)
    def get_fulfilment_info(self) -> str:
        return "Delivered digitally via download link."


# ============================================================================
# SECTION 3 TESTING
# ============================================================================
if __name__ == "__main__":
    print("=== Testing Section 3: Abstract Classes ===")

    # 3.3 Test the abstract class direct instantiation (Should fail)
    try:
        print("\nAttempting to instantiate Product directly...")
        generic_product = Product("P000", "Generic Item", 10.00, 5)
    except TypeError as e:
        print(f"Caught expected error: {e}")

    # Test concrete subclass instantiations
    print("\nInstantiating physical and digital products:")
    physical_item = PhysicalProduct("P101", "Mechanical Keyboard", 129.99, 15, 1.20)
    digital_item = DigitalProduct("D101", "Python Programming eBook", 19.99, 50, 15.40)

    physical_item.display_information()
    digital_item.display_information()