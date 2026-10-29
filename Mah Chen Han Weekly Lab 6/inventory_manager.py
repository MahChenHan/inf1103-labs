import json
import os

FILENAME = "inventory.json"

# 1. PRODUCT CLASS (Single Responsibility: Manage single product entity state)
class Product:
    """
    Represents and manages an individual product in the inventory.
    Demonstrates Encapsulation (Section 2.4) and Single Responsibility Principle (Section 2.5).
    """

    def __init__(self, product_id: str, name: str, price: float, stock: int):
        """Initializer setting protected instance attributes."""
        self._product_id = str(product_id)
        self.name = name
        self._price = float(price)
        self._stock = int(stock)

    # --- Properties (Getters) ---
    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def price(self) -> float:
        return self._price

    @property
    def stock(self) -> int:
        return self._stock

    # --- Public Methods ---
    def update_stock(self, new_stock: int) -> None:
        """Updates internal stock state after input validation."""
        if new_stock < 0:
            raise ValueError("Stock quantity cannot be negative!")
        self._stock = int(new_stock)

    def display_information(self) -> None:
        """Displays formatted single product information."""
        print("-" * 45)
        print(f"ID: {self._product_id}")
        print(f"Name: {self.name}")
        print(f"Price: ${self._price:.2f}")
        print(f"Stock: {self._stock}")
        print("-" * 45)

    # --- Serialization Helpers ---
    def to_dict(self) -> dict:
        """Converts Product instance attributes into a dictionary representation."""
        return {
            "name": self.name,
            "price": self._price,
            "stock": self._stock,
        }

    @classmethod
    def from_dict(cls, product_id: str, data: dict):
        """Instantiates a Product object from serialized dictionary data."""
        return cls(
            product_id=product_id,
            name=data["name"],
            price=data["price"],
            stock=data["stock"],
        )


# ============================================================================
# 2. PERSISTENCE & SYSTEM FUNCTIONS (To be encapsulated into Inventory in 2.6)
# ============================================================================
def load_inventory():
    """Handles JSON file loading."""
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                data = json.load(file)
                print(f"{FILENAME} found.")
                print("Inventory loaded successfully.\n")
                return {
                    item_id: Product.from_dict(item_id, details)
                    for item_id, details in data.items()
                }
        except Exception as e:
            print(f"Error loading {FILENAME}: {e}")
            print("Starting with empty inventory.\n")
            return {}
    else:
        print(f"{FILENAME} not found.")
        print("Starting with empty inventory.\n")
        return {}


def save_inventory(inventory, auto_exit=False):
    """Handles JSON file saving."""
    if auto_exit:
        print("Saving inventory before exit...")
    else:
        print("Saving inventory...")
    try:
        serialized_data = {
            item_id: product.to_dict() for item_id, product in inventory.items()
        }
        with open(FILENAME, "w") as file:
            json.dump(serialized_data, file, indent=4)
        print(f"Inventory saved successfully to {FILENAME}.\n")
    except Exception as e:
        print(f"Error saving inventory: {e}\n")


def display_all(inventory):
    """Prints listing of all current products."""
    print("\nCurrent Inventory")
    if not inventory:
        print("No items in inventory.\n")
        return
    for item_id, product in inventory.items():
        print(
            f"ID: {product.product_id} | Name: {product.name} | "
            f"Price: ${product.price:.2f} | Stock: {product.stock}"
        )
    print()


def add_product(inventory):
    """Gathers user input to add a new product."""
    print("\nAdd New Product")
    item_id = input("Product ID: ").strip()

    if item_id in inventory:
        print("Error: Product ID already exists!\n")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid price or stock quantity! Product not added.\n")
        return

    inventory[item_id] = Product(item_id, name, price, stock)
    print("Product added successfully!\n")


def update_stock(inventory):
    """Gathers user input to update product stock."""
    print("\nUpdate Stock")
    item_id = input("Enter Product ID: ").strip()

    if item_id in inventory:
        product = inventory[item_id]
        print("\nProduct Found:")
        print(f"Name: {product.name}")
        print(f"Current Stock: {product.stock}\n")

        try:
            new_stock = int(input("New Stock Quantity: "))
            product.update_stock(new_stock)
            print("Stock updated successfully!\n")
        except ValueError as e:
            print(f"Invalid input! {e}\n")
    else:
        print("Product not found.\n")


def search_product(inventory):
    """Searches for a product ID and delegates display to the Product object."""
    print("\nSearch Product")
    item_id = input("Enter Product ID: ").strip()

    if item_id in inventory:
        print("\nProduct Found")
        inventory[item_id].display_information()
        print()
    else:
        print("\nProduct not found.\n")


# ============================================================================
# 3. MAIN CLI DRIVER
# ============================================================================
def main():
    print("INVENTORY MANAGEMENT SYSTEM")
    inventory = load_inventory()

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
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            save_inventory(inventory, auto_exit=True)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option!\n")


if __name__ == "__main__":
    main()