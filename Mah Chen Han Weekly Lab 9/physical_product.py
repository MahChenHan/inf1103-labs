from can_be_shipped import CanBeShipped
from product import Product
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    """Represents a physical item requiring shipping and tracking weight."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float):
        super().__init__(product_id, name, price, stock, supplier)
        self._weight: float = float(weight)

    @property
    def weight(self) -> float:
        return self._weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self._weight:.2f} kg")
        print(f"Fulfilment: {self.get_fulfilment_info()}")
        print(f"Est. Shipping Cost: ${self.calculate_shipping_cost():.2f}")
        print("-" * 45)

    def get_product_type(self) -> str:
        return "Physical"

    def get_fulfilment_info(self) -> str:
        return "Requires physical warehouse dispatch and courier shipping."

    def calculate_shipping_cost(self) -> float:
        return 5.00 + (self._weight * 2.50)

    def to_dict(self) -> dict:
        return {
            "type": "physical",
            "name": self.name,
            "price": self._price,
            "stock": self._stock,
            "weight": self._weight,
            "supplier": self.supplier.to_dict(),
        }
