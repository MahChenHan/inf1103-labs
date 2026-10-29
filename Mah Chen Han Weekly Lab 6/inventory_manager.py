import json
import os

FILENAME = "inventory.json"

# 1. PRODUCT CLASS
# Single Responsibility: Represent and manage individual product data & state
class Product:
    """
    Represents an individual product.
    Enforces encapsulation through protected attributes (_attribute).
    """

    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self._product_id = str(product_id)
        self.name = name
        self._price = float(price)
        self._stock = int(stock)

    # --- Properties (Read-Only Getters) ---
    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def price(self) -> float:
        return self._price

    @property
    def stock(self) -> int:
        return self._stock

    # --- Public Encapsulated Methods ---
    def update_stock(self, new_stock: int) -> None:
        """Safely modifies internal stock state after input validation."""
        if new_stock < 0:
            raise ValueError("Stock quantity cannot be negative!")
        self._stock = int(new_stock)

    def display_information(self) -> None:
        """Displays formatted single product details."""
        print("-" * 45)
        print(f"ID: {self._product_id}")
        print(f"Name: {self.name}")
        print(f"Price: ${self._price:.2f}")
        print(f"Stock: {self._stock}")
        print("-" * 45)

    # --- Serialization Helpers ---
    def to_dict(self) -> dict:
        """Converts Product instance attributes into a dictionary for JSON writing."""
        return {
            "name": self.name,
            "price": self._price,
            "stock": self._stock,
        }

    @classmethod
    def from_dict(cls, product_id: str, data: dict):
        """Instantiates a Product object from dictionary data."""
        return cls(
            product_id=product_id,
            name=data["name"],
            price=data["price"],
            stock=data["stock"],
        )


# ============================================================================
# 2. INVENTORY CLASS
# Single Responsibility: Manage collection of Product objects and JSON storage
# ============================================================================
class Inventory:
    """
    Manages a collection of Product objects and file I/O operations.
    """

    def __init__(self, filename: str = FILENAME):
        self.filename = filename
        self.products: dict[str, Product] = {}
        self.load_inventory()

    def load_inventory(self) -> None:
        """Check whether JSON file exists and load Product instances."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    data = json.load(file)
                    self.products = {
                        item_id: Product.from_dict(item_id, details)
                        for item_id, details in data.items()
                    }
                print(f"{self.filename} found.")
                print("Inventory loaded successfully.\n")
            except Exception as e:
                print(f"Error loading {self.filename}: {e}")
                print("Starting with empty inventory.\n")
                self.products = {}
        else:
            print(f"{self.filename} not found.")
            print("Starting with empty inventory.\n")
            self.products = {}

    def save_inventory(self, auto_exit: bool = False) -> None:
        """Serializes Product instances and writes to JSON file."""
        if auto_exit:
            print("Saving inventory before exit...")
        else:
            print("Saving inventory...")

        try:
            serialized_data = {
                item_id: prod.to_dict() for item_id, prod in self.products.items()
            }
            with open(self.filename, "w") as file:
                json.dump(serialized_data, file, indent=4)
            print(f"Inventory saved successfully to {self.filename}.\n")
        except Exception as e:
            print(f"Error saving inventory: {e}\n")

    def add_product(self, product: Product) -> bool:
        """Adds a new Product object if ID does not already exist."""
        if product.product_id in self.products:
            print("Error: Product ID already exists!\n")
            return False
        self.products[product.product_id] = product
        print("Product added successfully!\n")
        return True

    def get_product(self, product_id: str) -> Product | None:
        """Retrieves a Product object by ID, or None if missing."""
        return self.products.get(product_id)

    def update_product_stock(self, product_id: str, new_stock: int) -> bool:
        """Finds product and updates stock using Product's encapsulated method."""
        product = self.get_product(product_id)
        if product:
            try:
                product.update_stock(new_stock)
                print("Stock updated successfully!\n")
                return True
            except ValueError as e:
                print(f"Invalid input! {e}\n")
                return False
        else:
            print("Product not found.\n")
            return False

    def display_all(self) -> None:
        """Displays all products in current inventory."""
        print("\nCurrent Inventory")
        if not self.products:
            print("No items in inventory.\n")
            return

        for product in self.products.values():
            print(
                f"ID: {product.product_id} | Name: {product.name} | "
                f"Price: ${product.price:.2f} | Stock: {product.stock}"
            )
        print()

# 3. INTERACTIVE CLI PROMPT HELPERS
def prompt_add_product(inventory: Inventory):
    """Gathers user input to construct and add a new Product object."""
    print("\nAdd New Product")
    item_id = input("Product ID: ").strip()

    if inventory.get_product(item_id):
        print("Error: Product ID already exists!\n")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid price or stock quantity! Product not added.\n")
        return

    new_product = Product(item_id, name, price, stock)
    inventory.add_product(new_product)


def prompt_update_stock(inventory: Inventory):
    """Gathers user input to update stock for an existing product."""
    print("\nUpdate Stock")
    item_id = input("Enter Product ID: ").strip()
    product = inventory.get_product(item_id)

    if product:
        print("\nProduct Found:")
        print(f"Name: {product.name}")
        print(f"Current Stock: {product.stock}\n")

        try:
            new_stock = int(input("New Stock Quantity: "))
            inventory.update_product_stock(item_id, new_stock)
        except ValueError:
            print("Invalid input! Stock not updated.\n")
    else:
        print("Product not found.\n")


def prompt_search_product(inventory: Inventory):
    """Gathers user input to search and display single product details."""
    print("\nSearch Product")
    item_id = input("Enter Product ID: ").strip()
    product = inventory.get_product(item_id)

    if product:
        print("\nProduct Found")
        product.display_information()
        print()
    else:
        print("\nProduct not found.\n")


# ============================================================================
# 4. MAIN CLI DRIVER
# ============================================================================
def main():
    print("INVENTORY MANAGEMENT SYSTEM")
    inventory = Inventory(FILENAME)

    while True:
        print("MENU")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")

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
            inventory.save_inventory()
        elif choice == "6":
            inventory.save_inventory(auto_exit=True)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option!\n")


if __name__ == "__main__":
    main()