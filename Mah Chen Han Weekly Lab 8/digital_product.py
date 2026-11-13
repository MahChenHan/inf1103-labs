from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """Represents a downloadable digital item with file size metrics."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float):
        super().__init__(product_id, name, price, stock, supplier)
        self._download_size: float = float(download_size)

    @property
    def download_size(self) -> float:
        return self._download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self._download_size:.2f} MB")
        print(f"Fulfilment: {self.get_fulfilment_info()}")
        print("-" * 45)

    def get_product_type(self) -> str:
        return "Digital"

    def get_fulfilment_info(self) -> str:
        return "Instant digital delivery via download link upon payment."

    def to_dict(self) -> dict:
        return {
            "type": "digital",
            "name": self.name,
            "price": self._price,
            "stock": self._stock,
            "download_size": self._download_size,
            "supplier": self.supplier.to_dict(),
        }
