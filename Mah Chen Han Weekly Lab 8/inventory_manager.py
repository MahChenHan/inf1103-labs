from abc import ABC, abstractmethod
import json
import os

FILENAME = "inventory.json"


# ============================================================================
# 1. SUPPLIER (Lab 8 - Section 2: ASSOCIATION)
# ============================================================================
class Supplier:
    """A supplier that provides products. Exists independently of any Product."""

    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self._supplier_id: str = str(supplier_id)
        self.name: str = name
        self.contact_email: str = contact_email

    @property
    def supplier_id(self) -> str:
        return self._supplier_id

    def display_information(self) -> None:
        print(f"Supplier ID: {self._supplier_id}")
        print(f"Supplier Name: {self.name}")
        print(f"Supplier Email: {self.contact_email}")

    def to_dict(self) -> dict[str, str]:
        return {
            "supplier_id": self._supplier_id,
            "name": self.name,
            "contact_email": self.contact_email,
        }


# ============================================================================
# 2. INTERFACE
# ============================================================================
class CanBeShipped(ABC):
    """Interface specifying shipping cost calculation contract."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Calculates and returns shipping cost based on product characteristics."""
        pass


# ============================================================================
# 3. ABSTRACT BASE CLASS
# ============================================================================
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
        print(f"ID: {self._product_id}")
        print(f"Name: {self.name}")
        print(f"Price: ${self._price:.2f}")
        print(f"Stock: {self._stock}")
        print(f"Supplier: {self.supplier.name} ({self.supplier.contact_email})")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Abstract method enforcing fulfilment details implementation."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Converts product instance to a dictionary for JSON persistence."""
        pass


# ============================================================================
# 4. CONCRETE SUBCLASSES
# ============================================================================
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


# ============================================================================
# 5. INVENTORY (Lab 8 - Section 3: AGGREGATION)
# ============================================================================
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
        """Displays summary of all stored products."""
        print("\nCurrent Inventory")
        if not self.products:
            print("No items in inventory.\n")
            return
        for product in self.products:
            ptype = "Physical" if isinstance(product, PhysicalProduct) else "Digital"
            print(
                f"[{ptype}] ID: {product.product_id} | "
                f"Name: {product.name} | Price: ${product.price:.2f} | "
                f"Stock: {product.stock} | Supplier: {product.supplier.name}"
            )
        print()


# ============================================================================
# 6. ORDER / ORDERLINE (Lab 8 - Section 4: COMPOSITION)
# ============================================================================
class OrderLine:
    """One product + quantity inside an Order. Only Order should create these."""

    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be at least 1.")
        self.product: Product = product   # association: refers to, not owns
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

    def display(self) -> None:
        print(f"  {self.product.name} x {self.quantity} "
              f"@ ${self.product.price:.2f} = ${self.calculate_subtotal():.2f}")


class Order:
    """COMPOSITION: Order creates, owns and removes its OrderLine objects."""

    def __init__(self, order_id: str):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)   # created INSIDE the Order
        self.order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for line in self.order_lines:
            if line.product.product_id == product_id:
                self.order_lines.remove(line)
                return True
        return False

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_order(self) -> None:
        print(f"Order {self.order_id}")
        if not self.order_lines:
            print("  (no order lines)")
        for line in self.order_lines:
            line.display()
        print(f"  TOTAL: ${self.calculate_total():.2f}")


# ============================================================================
# 7. CLI INTERACTION HELPERS
# ============================================================================
def prompt_supplier(inventory: Inventory) -> Supplier:
    """Reuses an existing Supplier if the ID is known, otherwise creates one."""
    supplier_id = input("Supplier ID: ").strip()
    if supplier_id in inventory.suppliers:
        supplier = inventory.suppliers[supplier_id]
        print(f"Using existing supplier: {supplier.name}")
        return supplier
    name = input("Supplier Name: ").strip()
    email = input("Supplier Email: ").strip()
    supplier = Supplier(supplier_id, name, email)
    inventory.suppliers[supplier_id] = supplier
    return supplier


def prompt_add_product(inventory: Inventory) -> None:
    print("\nAdd New Product")
    print("Select Product Type:")
    print("1. Physical Product")
    print("2. Digital Product")
    ptype_choice = input("Enter choice (1/2): ").strip()

    if ptype_choice not in ["1", "2"]:
        print("Invalid product type option! Product not added.\n")
        return

    item_id = input("Product ID: ").strip()
    if inventory.find_product(item_id):
        print("Error: Product ID already exists!\n")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        if ptype_choice == "1":
            weight = float(input("Weight (kg): "))
        else:
            download_size = float(input("Download Size (MB): "))
    except ValueError:
        print("Invalid numerical input! Product not added.\n")
        return

    supplier = prompt_supplier(inventory)
    if ptype_choice == "1":
        new_product: Product = PhysicalProduct(item_id, name, price, stock,
                                               supplier, weight)
    else:
        new_product = DigitalProduct(item_id, name, price, stock,
                                     supplier, download_size)
    inventory.add_product(new_product)


def prompt_update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    item_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(item_id)
    if product is None:
        print("Product not found.\n")
        return
    print("\nProduct Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}\n")
    try:
        new_stock = int(input("New Stock Quantity: "))
        inventory.update_product_stock(item_id, new_stock)
    except ValueError:
        print("Invalid input! Stock not updated.\n")


def prompt_search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    item_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(item_id)
    if product:
        print("\nProduct Found")
        product.display_information()
        print()
    else:
        print("\nProduct not found.\n")


def prompt_remove_product(inventory: Inventory) -> None:
    print("\nRemove Product")
    item_id = input("Enter Product ID: ").strip()
    inventory.remove_product(item_id)


# ============================================================================
# 8. MAIN CLI DRIVER
# ============================================================================
def main() -> None:
    print("INVENTORY MANAGEMENT SYSTEM (LAB 8)")
    inventory = Inventory(FILENAME)

    while True:
        print("MENU")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Remove Product")
        print("6. Save Inventory")
        print("7. Exit")

        choice = input("Enter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            prompt_add_product(inventory)
        elif choice == "3":
            prompt_update_stock(inventory)
        elif choice == "4":
            prompt_search_product(inventory)
        elif choice == "5":
            prompt_remove_product(inventory)
        elif choice == "6":
            inventory.save_inventory()
        elif choice == "7":
            inventory.save_inventory(auto_exit=True)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option!\n")


if __name__ == "__main__":
    main()
