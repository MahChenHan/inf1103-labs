from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


class ProductFactory:
    """The ONE place that decides which Product subclass to build."""

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier,
               weight_or_size: float = 0.0) -> Product:
        """weight_or_size = weight in kg (physical) or download size in MB (digital)."""
        product_type = product_type.strip().lower()
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity,
                                   supplier, weight_or_size)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity,
                                  supplier, weight_or_size)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
