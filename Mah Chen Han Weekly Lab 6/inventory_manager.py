import json
import os

FILENAME = "inventory.json"


class Product:
    """
    Represents and manages an individual product in the inventory.
    Enforces Encapsulation (Section 2.4) and the Single Responsibility Principle (SRP).
    """

    def __init__(self, product_id: str, name: str, price: float, stock: int):
        """Initializer (constructor) setting private/protected attributes."""
        # Using leading underscore convention (_attribute) to signal private state
        self._product_id = str(product_id)
        self.name = name
        self._price = float(price)
        self._stock = int(stock)

    # --- Encapsulated Properties (Read-Only Accessors) ---
    @property
    def product_id(self) -> str:
        """Read-only access to product_id."""
        return self._product_id

    @property
    def price(self) -> float:
        """Read-only access to price."""
        return self._price

    @property
    def stock(self) -> int:
        """Read-only access to stock quantity."""
        return self._stock

    # --- Encapsulated Public Methods ---
    def update_stock(self, new_stock: int) -> None:
        """
        Encapsulation in Action:
        Controls how stock is updated from outside the class.
        Validates input before modifying internal self._stock state.
        """
        if new_stock < 0:
            raise ValueError("Stock quantity cannot be negative!")
        
        self._stock = int(new_stock)

    def display_information(self) -> None:
        """Displays formatted information for a single product."""
        print("-" * 45)
        print(f"ID: {self._product_id}")
        print(f"Name: {self.name}")
        print(f"Price: ${self._price:.2f}")
        print(f"Stock: {self._stock}")
        print("-" * 45)

    # --- Serialization Helper Methods ---
    def to_dict(self) -> dict:
        """Converts Product instance attributes into a dictionary for JSON saving."""
        return {
            "name": self.name,
            "price": self._price,
            "stock": self._stock,
        }

    @classmethod
    def from_dict(cls, product_id: str, data: dict):
        """Instantiates a Product object directly from dictionary data."""
        return cls(
            product_id=product_id,
            name=data["name"],
            price=data["price"],
            stock=data["stock"],
        )


def load_inventory():
    """Check whether inventory.json exists and load it as Product objects."""
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
    """Save the current inventory dictionary to inventory.json."""
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
    """Display all products in the current inventory."""
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
    """Add a new product object to the inventory dictionary via user input."""
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
    """Update stock quantity safely using Product's encapsulated update_stock method."""
    print("\nUpdate Stock")
    item_id = input("Enter Product ID: ").strip()

    if item_id in inventory:
        product = inventory[item_id]
        print("\nProduct Found:")
        print(f"Name: {product.name}")
        print(f"Current Stock: {product.stock}\n")

        try:
            new_stock = int(input("New Stock Quantity: "))
            # Enforces Encapsulation: Modifies internal state via class method
            product.update_stock(new_stock)
            print("Stock updated successfully!\n")
        except ValueError as e:
            print(f"Invalid input! {e}\n")
    else:
        print("Product not found.\n")


def search_product(inventory):
    """Search and display details of a product by ID."""
    print("\nSearch Product")
    item_id = input("Enter Product ID: ").strip()

    if item_id in inventory:
        print("\nProduct Found")
        inventory[item_id].display_information()
        print()
    else:
        print("\nProduct not found.\n")


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