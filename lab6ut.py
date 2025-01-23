import unittest
from lab6 import Equipment, InvalidEquipmentCostError

class TestEquipment(unittest.TestCase):

    def test_addition(self):
        eq1 = Equipment(cost=1000)
        eq2 = Equipment(cost=2000)
        self.assertEqual(eq1 + eq2, 3000)

    def test_subtraction(self):
        eq1 = Equipment(cost=3000)
        eq2 = Equipment(cost=1000)
        self.assertEqual(eq1 - eq2, 2000)

    def test_multiplication(self):
        eq1 = Equipment(cost=500)
        self.assertEqual(eq1 * 2, 1000)

    def test_division(self):
        eq1 = Equipment(cost=1000)
        self.assertEqual(eq1 / 2, 500)

    def test_invalid_addition(self):
        eq1 = Equipment(cost=1000)
        with self.assertRaises(TypeError):
            eq1 + "NotEquipment"

    def test_invalid_division(self):
        eq1 = Equipment(cost=1000)
        with self.assertRaises(ValueError):
            eq1 / 0

if __name__ == "__main__":
    unittest.main()