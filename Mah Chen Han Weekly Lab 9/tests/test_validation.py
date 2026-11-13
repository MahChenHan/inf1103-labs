"""Lab 9 Section 4: validation tests."""
import unittest

from order import Order
from product_factory import ProductFactory
from supplier import Supplier

SUPPLIER = Supplier("S001", "TechSupply", "sales@techsupply.sg")


def make_product(price: float = 10.0, stock: int = 5, product_type: str = "physical"):
    return ProductFactory.create(product_type, "P001", "Desk Lamp", price,
                                 stock, SUPPLIER, 1.0)


class TestProductValidation(unittest.TestCase):

    def test_valid_product_is_created(self):
        self.assertEqual(make_product().price, 10.0)

    def test_zero_price_rejected(self):
        with self.assertRaises(ValueError) as context:
            make_product(price=0)
        self.assertEqual(str(context.exception), "Price must be greater than zero.")

    def test_negative_price_rejected(self):
        with self.assertRaises(ValueError):
            make_product(price=-5)

    def test_negative_stock_rejected_on_creation(self):
        with self.assertRaises(ValueError) as context:
            make_product(stock=-1)
        self.assertEqual(str(context.exception), "Stock quantity cannot be negative.")

    def test_zero_stock_allowed(self):
        self.assertEqual(make_product(stock=0).stock, 0)

    def test_negative_stock_rejected_on_update(self):
        product = make_product()
        with self.assertRaises(ValueError):
            product.update_stock(-3)
        self.assertEqual(product.stock, 5)   # unchanged after rejected update

    def test_digital_product_keeps_the_same_rules(self):
        """LSP: DigitalProduct must not skip the parent's validation."""
        with self.assertRaises(ValueError):
            make_product(stock=-1, product_type="digital")


class TestOrderLineValidation(unittest.TestCase):

    def test_zero_quantity_rejected(self):
        order = Order("O001")
        with self.assertRaises(ValueError) as context:
            order.add_order_line(make_product(), 0)
        self.assertEqual(str(context.exception), "Quantity must be greater than zero.")
        self.assertEqual(len(order.order_lines), 0)

    def test_negative_quantity_rejected(self):
        with self.assertRaises(ValueError):
            Order("O002").add_order_line(make_product(), -2)


if __name__ == "__main__":
    unittest.main()
