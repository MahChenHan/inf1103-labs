"""Lab 9 Section 5.2: load products from a CSV file without crashing."""
import csv

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Reads products from CSV, creates each through ProductFactory and adds it.
    Bad rows are reported and skipped; a missing file is reported, not fatal."""
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)                   # skip the header row
            for row_number, row in enumerate(reader, start=2):
                try:
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(product_type, product_id,
                                                    name, float(price),
                                                    int(stock), supplier)
                except ValueError as error:
                    print(f"Skipped row {row_number} {row}: {error}")
                    continue
                if inventory.add_product(product):
                    loaded += 1
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
