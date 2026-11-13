"""Entry point: menu-driven CLI for the Inventory Management System."""
from inventory import FILENAME, Inventory
from product_factory import ProductFactory
from supplier import Supplier


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
    product_type = "physical" if ptype_choice == "1" else "digital"
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        if product_type == "physical":
            weight_or_size = float(input("Weight (kg): "))
        else:
            weight_or_size = float(input("Download Size (MB): "))
    except ValueError:
        print("Invalid numerical input! Product not added.\n")
        return

    supplier = prompt_supplier(inventory)
    new_product = ProductFactory.create(product_type, item_id, name, price,
                                        stock, supplier, weight_or_size)
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


def main() -> None:
    print("INVENTORY MANAGEMENT SYSTEM (LAB 9)")
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
