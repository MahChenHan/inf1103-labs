"""Lab 9 Section 2: Strategy pattern tests.
Run from the project folder with:  python -m unittest discover tests -v
"""
import unittest

from bulk_discount import BulkDiscount
from no_discount import NoDiscount
from order import Order
from percentage_discount import PercentageDiscount
from physical_product import PhysicalProduct
from supplier import Supplier


def make_order_totalling_250() -> Order:
    supplier = Supplier("S001", "TechSupply", "sales@techsupply.sg")
    lamp = PhysicalProduct("P001", "Desk Lamp", 50.0, 10, supplier, 1.0)
    order = Order("O001")
    order.add_order_line(lamp, 5)          # 5 x 50 = 250
    return order


class TestDiscountStrategies(unittest.TestCase):

    def test_no_discount_returns_total_unchanged(self):
        self.assertEqual(NoDiscount().apply(100.0), 100.0)

    def test_percentage_discount(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(100.0), 90.0)

    def test_bulk_discount_applies_at_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(200.0), 180.0)

    def test_bulk_discount_ignored_below_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(150.0), 150.0)


class TestOrderUsesStrategy(unittest.TestCase):

    def test_order_defaults_to_no_discount(self):
        order = make_order_totalling_250()
        self.assertIsInstance(order.discount, NoDiscount)
        self.assertEqual(order.calculate_total(), 250.0)

    def test_bulk_then_switch_to_percentage(self):
        order = make_order_totalling_250()
        order.set_discount(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230.0)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_strategy_given_in_constructor(self):
        order = Order("O002", PercentageDiscount(50))
        supplier = Supplier("S001", "TechSupply", "sales@techsupply.sg")
        order.add_order_line(PhysicalProduct("P9", "Box", 10.0, 5, supplier, 1.0), 2)
        self.assertAlmostEqual(order.calculate_total(), 10.0)

    def test_two_orders_can_share_one_strategy_object(self):
        shared = PercentageDiscount(10)
        order_a, order_b = Order("A", shared), Order("B", shared)
        self.assertIs(order_a.discount, order_b.discount)


if __name__ == "__main__":
    unittest.main()
