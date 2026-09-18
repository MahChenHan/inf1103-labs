total_inventory = 0
failed_entries = 0

while True:
    user_input = input("Enter stock quantity (or 'quit' to exit): ")
    
    if user_input.lower() == "quit":
        break

    if not user_input.isdigit():
        print("Error: Invalid input. Please enter a positive whole number.")
        failed_entries += 1
        continue
        
    quantity = int(user_input)
    
    total_inventory += quantity
    print(f"Current total inventory: {total_inventory} units.")
    
    if total_inventory > 500:
        print("\nALERT: Storage capacity exceeded! Total inventory over 500 units.")
        break

print("\n--- Audit Summary Report ---")
print(f"Total Units Processed: {total_inventory}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")