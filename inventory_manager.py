import json
import os

FILENAME = "inventory.json"


def load_inventory():
    """Check whether inventory.json exists and load it; otherwise return default inventory."""
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                print(f"{FILENAME} found.")
                print("Inventory loaded successfully.\n")
                return json.load(file)
        except Exception as e:
            print(f"Error loading {FILENAME}: {e}")
            print("Starting with empty inventory.\n")
            return {}
    else:
        print(f"{FILENAME} not found.")
        print("Starting with empty inventory.\n")
        return {
            "P001": {"name": "Laptop", "price": 1200.00, "stock": 15},
            "P002": {"name": "Mouse", "price": 25.50, "stock": 40},
            "P003": {"name": "Keyboard", "price": 45.00, "stock": 25},
        }


def save_inventory(inventory, auto_exit=False):
    """Save the current inventory dictionary to inventory.json."""
    if auto_exit:
        print("Saving inventory before exit...")
    else:
        print("Saving inventory...")
    try:
        with open(FILENAME, "w") as file:
            json.dump(inventory, file, indent=4)
        print(f"Inventory saved successfully to {FILENAME}.\n")
    except Exception as e:
        print(f"Error saving inventory: {e}\n")


def display_all(inventory):
    """Display all products in the current inventory."""
    print("\nCurrent Inventory")
    if not inventory:
        print("No items in inventory.\n")
        return
    for item_id, details in inventory.items():
        print(
            f"ID: {item_id} | Name: {details['name']} | Price: ${details['price']:.2f} | Stock: {details['stock']}"
        )
    print()


def add_product(inventory):
    """Add a new product to the inventory dictionary."""
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

    inventory[item_id] = {"name": name, "price": price, "stock": stock}
    print("Product added successfully!\n")


def update_stock(inventory):
    """Update stock quantity of an existing product."""
    print("\nUpdate Stock")
    item_id = input("Enter Product ID: ").strip()

    if item_id in inventory:
        print("\nProduct Found:")
        print(f"Name: {inventory[item_id]['name']}")
        print(f"Current Stock: {inventory[item_id]['stock']}\n")

        try:
            new_stock = int(input("New Stock Quantity: "))
            inventory[item_id]["stock"] = new_stock
            print("Stock updated successfully!\n")
        except ValueError:
            print("Invalid input! Stock not updated.\n")
    else:
        print("Product not found.\n")


def search_product(inventory):
    """Search and display details of a product by ID."""
    print("\nSearch Product")
    item_id = input("Enter Product ID: ").strip()

    if item_id in inventory:
        print("\nProduct Found")
        print("-" * 45)
        print(f"ID: {item_id}")
        print(f"Name: {inventory[item_id]['name']}")
        print(f"Price: ${inventory[item_id]['price']:.2f}")
        print(f"Stock: {inventory[item_id]['stock']}")
        print("-" * 45 + "\n")
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