"""Lab 8 tests: association, aggregation, composition, LSP, polymorphism.
Run with:  python test_lab8.py
"""
from inventory_manager import (Supplier, PhysicalProduct, DigitalProduct, Inventory)


def header(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ---------------------------------------------------------------- Section 2
def test_association() -> None:
    header("SECTION 2: ASSOCIATION (Supplier -- Product)")
    supplier = Supplier("S001", "TechSupply Pte Ltd", "sales@techsupply.sg")

    laptop = PhysicalProduct("P100", "Laptop", 1200.0, 10, supplier, 1.8)
    ebook = DigitalProduct("D100", "Python eBook", 29.9, 999, supplier, 15.5)

    print("Supplier seen through each product:")
    laptop.supplier.display_information()
    ebook.supplier.display_information()

    print(f"\nSame Supplier object shared? {laptop.supplier is ebook.supplier}")
    print(f"Supplier is a separate object from product? {laptop is not supplier}")

    del supplier   # deletes the NAME only, not the object
    print("\nAfter `del supplier`:")
    print(f"Laptop still knows its supplier: {laptop.supplier.name}")
    print(f"eBook still knows its supplier:  {ebook.supplier.name}")


# ---------------------------------------------------------------- Section 3
def test_aggregation() -> None:
    header("SECTION 3: AGGREGATION (Inventory <>-- Product)")
    supplier = Supplier("S002", "GadgetHub", "hello@gadgethub.sg")

    mouse = PhysicalProduct("P200", "Mouse", 25.5, 40, supplier, 0.2)
    print(f"Product created BEFORE any inventory: {mouse.name}")

    inventory_a = Inventory(filename=None)
    inventory_b = Inventory(filename=None)

    inventory_a.add_product(mouse)
    print(f"In A? {inventory_a.find_product('P200') is not None}")

    removed = inventory_a.remove_product("P200")
    print(f"In A after removal? {inventory_a.find_product('P200') is not None}")
    print(f"Product still usable: {removed.name}, stock {removed.stock}")
    removed.update_stock(35)
    print(f"Stock updated outside any inventory: {mouse.stock}")

    inventory_b.add_product(mouse)
    print(f"Same object now in B? {inventory_b.find_product('P200') is mouse}")


if __name__ == "__main__":
    test_association()
    test_aggregation()
