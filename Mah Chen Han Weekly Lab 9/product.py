from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    """Abstract base class for all products in the system."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier):
        self._product_id: str = str(product_id)
        self.name: str = name
        self._price: float = float(price)
        self._stock: int = int(stock)
        # ASSOCIATION: Product keeps a reference to a Supplier it does not own
        self.supplier: Supplier = supplier

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
        """Updates internal stock state after input validation."""
        if new_stock < 0:
            raise ValueError("Stock quantity cannot be negative!")
        self._stock = int(new_stock)

    def display_information(self) -> None:
        """Displays common product information."""
        print("-" * 45)
        print(f"Type: {self.get_product_type()}")
        print(f"ID: {self._product_id}")
        print(f"Name: {self.name}")
        print(f"Price: ${self._price:.2f}")
        print(f"Stock: {self._stock}")
        print(f"Supplier: {self.supplier.name} ({self.supplier.contact_email})")

    @abstractmethod
    def get_product_type(self) -> str:
        """Returns a readable label for the product type (polymorphic)."""
        pass

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Abstract method enforcing fulfilment details implementation."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Converts product instance to a dictionary for JSON persistence."""
        pass
