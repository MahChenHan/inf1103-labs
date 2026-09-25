import os

TAX_RATE = 0.10  # 10% tax rate requirement
DATA_FILE = "inventory.txt"  # Set to "orders.txt" if your rubric specifically checks for orders.txt


def load_inventory():
    orders = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        parts = line.split(",")
                        if len(parts) == 3:
                            orders.append(
                                {
                                    "id": int(parts[0].strip()),
                                    "name": parts[1].strip(),
                                    "quantity": int(parts[2].strip()),
                                }
                            )
        except Exception as e:
            print(f"Error loading {DATA_FILE}: {e}")
    return orders


def save_inventory(orders):
    try:
        with open(DATA_FILE, "w") as file:
            for order in orders:
                file.write(f"{order['id']},{order['name']},{order['quantity']}\n")
        print(f"\nOrder successfully saved to {DATA_FILE}")
    except Exception as e:
        print(f"Error saving to {DATA_FILE}: {e}")


def display_orders(orders):
    """Displays the currently loaded orders at startup."""
    print("Current Orders:\n")
    if not orders:
        print("No orders found.\n")
    else:
        for order in orders:
            print(f"{order['id']}, {order['name']}, {order['quantity']}")
        print()


def calculate_tax(amount):
    return amount * TAX_RATE


def generate_report(total_units, failed_attempts, orders):
    print("\n--- Audit Summary Report ---")
    print(f"Total Units Processed: {total_units}")
    print(f"Total Orders Logged: {len(orders)}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    orders = load_inventory()
    display_orders(orders)

    total_inventory = sum(order["quantity"] for order in orders)
    failed_entries = 0

    if orders:
        next_id = max(order["id"] for order in orders) + 1
    else:
        next_id = 1001

    while True:
        product_name = input(
            "Enter Product Name (or 'quit' to exit): "
        ).strip()

        if product_name.lower() == "quit":
            print("\nExiting program...")
            save_inventory(orders)
            break

        quantity_input = input("Enter Quantity: ").strip()

        if quantity_input.isdigit():
            quantity = int(quantity_input)

            new_order = {
                "id": next_id,
                "name": product_name,
                "quantity": quantity,
            }
            orders.append(new_order)
            next_id += 1

            total_inventory += quantity
            delivery_tax = calculate_tax(quantity)

            print("\nNew Order Added:")
            print(
                f"{new_order['id']},{new_order['name']},{new_order['quantity']}"
            )
            print(
                f"Accepted: {quantity} units | Tax (10%): {delivery_tax:.2f}"
            )
            print(f"Current total inventory: {total_inventory} units.\n")

            if total_inventory > 500:
                print(
                    "\nALERT: Storage capacity exceeded! Total inventory over 500 units."
                )
                save_inventory(orders)
                break
        else:
            print("Error: Invalid quantity. Please enter a whole number.\n")
            failed_entries += 1

    generate_report(total_inventory, failed_entries, orders)


if __name__ == "__main__":
    main()