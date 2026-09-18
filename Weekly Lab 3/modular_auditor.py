TAX_RATE = 0.10  # 10% tax rate requirement


def get_valid_input():
    user_input = input("Enter stock quantity (or 'quit' to exit): ").strip()

    if user_input.lower() == "quit":
        return "quit"

    if not user_input.isdigit():
        print("Error: Invalid input. Please enter a positive whole number.")
        return None

    return int(user_input)


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * TAX_RATE


def generate_report(total_units, failed_attempts):
    print("\n--- Audit Summary Report ---")
    print(f"Total Units Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    total_inventory = 0
    failed_entries = 0

    while True:
        entry = get_valid_input()

        if entry == "quit":
            break
        elif entry is None:
            failed_entries += 1
        else:

            total_inventory = process_delivery(total_inventory, entry)
            delivery_tax = calculate_tax(entry)

            print(f"Accepted: {entry} units | Tax (10%): {delivery_tax:.2f}")
            print(f"Current total inventory: {total_inventory} units.")

            if total_inventory > 500:
                print(
                    "\nALERT: Storage capacity exceeded! Total inventory over 500 units."
                )
                break

    generate_report(total_inventory, failed_entries)


if __name__ == "__main__":
    main()