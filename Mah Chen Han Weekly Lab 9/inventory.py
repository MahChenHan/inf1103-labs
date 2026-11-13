import json
import os

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier

FILENAME = "inventory.json"


DEFAULT_SUPPLIER = Supplier("S000", "Unknown Supplier", "n/a")


def product_from_dict(product_id: str, data: dict,
                      suppliers: dict[str, Supplier]) -> Product:
    """Builds the right Product subclass from a JSON record.

    `suppliers` caches Supplier objects by ID so products from the same
    supplier share ONE Supplier object (one supplier -> many products).
    """
    supplier_data = data.get("supplier")
    if supplier_data:
        sid = supplier_data["supplier_id"]
        if sid not in suppliers:
            suppliers[sid] = Supplier(sid, supplier_data["name"],
                                      supplier_data["contact_email"])
        supplier = suppliers[sid]
    else:
        supplier = DEFAULT_SUPPLIER  # old Lab 7 records have no supplier

    product_type = data.get("type", "physical")
    if product_type == "physical":
        return PhysicalProduct(product_id, data["name"], data["price"],
                               data["stock"], supplier, data.get("weight", 0.0))
    elif product_type == "digital":
        return DigitalProduct(product_id, data["name"], data["price"],
                              data["stock"], supplier,
                              data.get("download_size", 0.0))
    else:
        raise ValueError(f"Unknown product type: {product_type}")


class Inventory:
    """Groups Product objects. Does NOT create or own their lifecycle."""

    def __init__(self, filename: str | None = FILENAME):
        self.filename: str | None = filename
        self.products: list[Product] = []
        self.suppliers: dict[str, Supplier] = {}
        if filename:
            self.load_inventory()

    def load_inventory(self) -> None:
        """Loads product records from JSON file and instantiates subclasses."""
        if self.filename and os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    data = json.load(file)
                self.products = [
                    product_from_dict(item_id, details, self.suppliers)
                    for item_id, details in data.items()
                ]
                print(f"{self.filename} found.")
                print("Inventory loaded successfully.\n")
            except Exception as e:
                print(f"Error loading {self.filename}: {e}")
                print("Starting with empty inventory.\n")
                self.products = []
        else:
            print(f"{self.filename} not found.")
            print("Starting with empty inventory.\n")
            self.products = []

    def save_inventory(self, auto_exit: bool = False) -> None:
        """Serializes Product instances to dictionary format and writes to JSON."""
        if not self.filename:
            return
        print("Saving inventory before exit..." if auto_exit else "Saving inventory...")
        try:
            serialized_data = {p.product_id: p.to_dict() for p in self.products}
            with open(self.filename, "w") as file:
                json.dump(serialized_data, file, indent=4)
            print(f"Inventory saved successfully to {self.filename}.\n")
        except Exception as e:
            print(f"Error saving inventory: {e}\n")

    def add_product(self, product: Product) -> bool:
        """Adds an EXISTING Product object (created outside the Inventory)."""
        if self.find_product(product.product_id):
            print("Error: Product ID already exists!\n")
            return False
        self.products.append(product)
        print("Product added successfully!\n")
        return True

    def remove_product(self, product_id: str) -> Product | None:
        """Removes the reference only. The Product object itself survives."""
        product = self.find_product(product_id)
        if product is None:
            print("Product not found.\n")
            return None
        self.products.remove(product)
        print(f"Product {product_id} removed from inventory.\n")
        return product

    def find_product(self, product_id: str) -> Product | None:
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None

    def update_product_stock(self, product_id: str, new_stock: int) -> bool:
        """Delegates stock update to the target Product object."""
        product = self.find_product(product_id)
        if product is None:
            print("Product not found.\n")
            return False
        try:
            product.update_stock(new_stock)
            print("Stock updated successfully!\n")
            return True
        except ValueError as e:
            print(f"Invalid input! {e}\n")
            return False

    def display_all(self) -> None:
        """Summary list. Polymorphic: no isinstance() checks."""
        print("\nCurrent Inventory")
        if not self.products:
            print("No items in inventory.\n")
            return
        for product in self.products:
            print(
                f"[{product.get_product_type()}] ID: {product.product_id} | "
                f"Name: {product.name} | Price: ${product.price:.2f} | "
                f"Stock: {product.stock} | Supplier: {product.supplier.name}"
            )
        print()

    def display_all_products(self) -> None:
        """Full details. Each Product picks its own display_information()."""
        for product in self.products:
            product.display_information()
