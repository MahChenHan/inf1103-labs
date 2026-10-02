import os

FILENAME = "inventory.json"


def init_inventory():
    """Initialize default inventory with dictionary data structures."""
    return {
        "P001": {"name": "Laptop", "price": 1200.00, "stock": 15},
        "P002": {"name": "Mouse", "price": 25.50, "stock": 40},
        "P003": {"name": "Keyboard", "price": 45.00, "stock": 25},
    }


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


def main():
    print("INVENTORY MANAGEMENT SYSTEM")
    # Phase A: Starting with initial dictionary structure
    inventory = init_inventory()

    while True:
        print("MENU")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Exit")

        choice = input("Enter option: ").strip()

        if choice == "1":
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid option!\n")


if __name__ == "__main__":
    main()