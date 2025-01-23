import unittest
from lab4 import ProEquip


class MyTestCase(unittest.TestCase):
    def test_items_info(self):
        self.pila =  ProEquip("Пила экста","зуб15","14.12.2024", 1200, "ogo")
        self.test_string = "Номер = 1 название = Пила экста модель = зуб15 Дата покупки = 14.12.2024 цена = 1200 вид = ogo"
        self.assertEqual(self.pila.__str__(), self.test_string)  # add assertion here


if __name__ == '__main__':
    unittest.main()