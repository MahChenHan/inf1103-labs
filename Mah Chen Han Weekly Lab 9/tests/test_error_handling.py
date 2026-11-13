"""Lab 9 Section 5: exception handling tests (user input and CSV loading)."""
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from input_helpers import get_non_negative_int, get_positive_float
from inventory import Inventory
from product_loader import load_products
from supplier import Supplier

SUPPLIER = Supplier("S001", "TechSupply", "sales@techsupply.sg")
PRODUCTS_CSV = os.path.join(os.path.dirname(__file__), "..", "products.csv")


def run_and_capture(function, *args) -> tuple[object, str]:
    """Runs a function and returns (its result, everything it printed)."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        result = function(*args)
    return result, buffer.getvalue()


class TestGetPositiveFloat(unittest.TestCase):

    @patch("builtins.input", side_effect=["abc", "-5", "12.50"])
    def test_keeps_asking_until_valid(self, mock_input):
        value, output = run_and_capture(get_positive_float, "Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(mock_input.call_count, 3)
        self.assertEqual(output.splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    @patch("builtins.input", side_effect=["0", "3"])
    def test_zero_is_rejected(self, mock_input):
        value, _ = run_and_capture(get_positive_float, "Price: ")
        self.assertEqual(value, 3.0)


class TestGetNonNegativeInt(unittest.TestCase):

    @patch("builtins.input", side_effect=["ten", "-1", "2.5", "0"])
    def test_keeps_asking_until_valid(self, mock_input):
        value, _ = run_and_capture(get_non_negative_int, "Stock: ")
        self.assertEqual(value, 0)
        self.assertEqual(mock_input.call_count, 4)


class TestLoadProducts(unittest.TestCase):

    def test_valid_rows_load_and_bad_rows_are_skipped(self):
        inventory = Inventory(filename=None)
        _, output = run_and_capture(load_products, PRODUCTS_CSV, inventory, SUPPLIER)
        loaded_ids = [p.product_id for p in inventory.products]
        self.assertEqual(loaded_ids, ["P001", "D001", "P003"])
        self.assertIn("Unknown product type: service", output)
        self.assertIn("could not convert string to float: 'abc'", output)
        self.assertIn("3 products loaded.", output)
        self.assertTrue(output.rstrip().endswith("Load attempt finished."))

    def test_missing_file_is_handled_gracefully(self):
        inventory = Inventory(filename=None)
        _, output = run_and_capture(load_products, "no_such_file.csv",
                                    inventory, SUPPLIER)
        self.assertIn("Products file not found: no_such_file.csv", output)
        self.assertIn("Load attempt finished.", output)       # finally ran
        self.assertNotIn("products loaded", output)           # else did not run
        self.assertEqual(inventory.products, [])

    def test_row_with_wrong_number_of_columns_is_skipped(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                         newline="") as temp:
            temp.write("product_type,product_id,name,price,stock_quantity\n")
            temp.write("physical,P010,Too Short\n")
            temp.write("digital,D010,E-book,9.99,50\n")
        try:
            inventory = Inventory(filename=None)
            _, output = run_and_capture(load_products, temp.name, inventory, SUPPLIER)
            self.assertEqual([p.product_id for p in inventory.products], ["D010"])
            self.assertIn("1 products loaded.", output)
        finally:
            os.remove(temp.name)


class TestInventoryFileErrors(unittest.TestCase):

    def test_missing_inventory_file_starts_empty(self):
        _, output = run_and_capture(Inventory, "missing_inventory.json")
        self.assertIn("missing_inventory.json not found.", output)

    def test_corrupt_inventory_file_starts_empty(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as temp:
            temp.write("{ this is not json")
        try:
            inventory, output = run_and_capture(Inventory, temp.name)
            self.assertEqual(inventory.products, [])
            self.assertIn("Error loading", output)
        finally:
            os.remove(temp.name)


if __name__ == "__main__":
    unittest.main()
