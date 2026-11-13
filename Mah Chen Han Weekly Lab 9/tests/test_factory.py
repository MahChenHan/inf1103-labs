"""Lab 9 Section 3: Factory pattern tests."""
import unittest

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from supplier import Supplier

SUPPLIER = Supplier("S001", "TechSupply", "sales@techsupply.sg")


class TestProductFactory(unittest.TestCase):

    def test_creates_physical_product(self):
        product = ProductFactory.create("physical", "P001", "Desk Lamp",
                                        25.0, 10, SUPPLIER, 1.2)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.weight, 1.2)

    def test_creates_digital_product(self):
        product = ProductFactory.create("digital", "D001", "Photo Editor",
                                        49.9, 100, SUPPLIER, 900.0)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.download_size, 900.0)

    def test_returns_product_base_type(self):
        product = ProductFactory.create("physical", "P002", "Chair",
                                        80.0, 3, SUPPLIER)
        self.assertIsInstance(product, Product)

    def test_type_is_case_insensitive(self):
        product = ProductFactory.create(" Digital ", "D002", "Font Pack",
                                        5.0, 50, SUPPLIER)
        self.assertIsInstance(product, DigitalProduct)

    def test_unknown_type_raises_clear_value_error(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Installation",
                                  30.0, 5, SUPPLIER)
        self.assertEqual(str(context.exception), "Unknown product type: service")


if __name__ == "__main__":
    unittest.main()
