"""Lab 8 tests: association, aggregation, composition, LSP, polymorphism.
Run with:  python test_lab8.py
"""
from inventory_manager import (Supplier, Product, PhysicalProduct,
                               DigitalProduct, Inventory, Order)


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


# ---------------------------------------------------------------- Section 4
def test_composition() -> None:
    header("SECTION 4: COMPOSITION (Order <>-- OrderLine)")
    supplier = Supplier("S003", "SoftWorld", "support@softworld.sg")
    keyboard = PhysicalProduct("P300", "Keyboard", 89.9, 25, supplier, 0.9)
    antivirus = DigitalProduct("D300", "Antivirus Licence", 49.0, 500, supplier, 250.0)

    order1 = Order("O001")
    order1.add_order_line(keyboard, 2)
    order1.add_order_line(antivirus, 1)
    order1.display_order()

    order2 = Order("O002")
    order2.add_order_line(keyboard, 1)   # same Product, different Order
    order2.display_order()

    line_a = order1.order_lines[0]
    line_b = order2.order_lines[0]
    print(f"\nSame OrderLine object?   {line_a is line_b}  "
          f"(ids {id(line_a)} vs {id(line_b)})")
    print(f"Same Product object?     {line_a.product is line_b.product}  "
          f"(ids {id(line_a.product)} vs {id(line_b.product)})")

    print("\nRemoving keyboard line from O001 via the Order:")
    order1.remove_order_line("P300")
    order1.display_order()
    print(f"Keyboard product still exists: {keyboard.name}")


# ---------------------------------------------------------------- Section 6
def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def test_lsp() -> None:
    header("SECTION 6: LSP (substitutability)")
    supplier = Supplier("S004", "MixedGoods", "mix@goods.sg")
    phys = PhysicalProduct("P400", "Monitor", 250.0, 8, supplier, 4.5)
    digi = DigitalProduct("D400", "Photo Editor", 79.0, 100, supplier, 900.0)

    for product in (phys, digi):
        show_product_details(product)       # same function, both work
        product.update_stock(product.stock + 5)   # parent contract kept
        print(f"{product.name} stock after update_stock: {product.stock}\n")


# ---------------------------------------------------------------- Section 7
def test_polymorphism() -> None:
    header("SECTION 7: POLYMORPHISM (one loop, no isinstance)")
    supplier = Supplier("S005", "AllInOne", "info@allinone.sg")
    inventory = Inventory(filename=None)
    inventory.add_product(PhysicalProduct("P500", "Headphones", 120.0, 12, supplier, 0.3))
    inventory.add_product(DigitalProduct("D500", "Music Pack", 9.9, 1000, supplier, 300.0))

    for product in inventory.products:
        product.display_information()
        print(product.get_fulfilment_info())


if __name__ == "__main__":
    test_association()
    test_aggregation()
    test_composition()
    test_lsp()
    test_polymorphism()
