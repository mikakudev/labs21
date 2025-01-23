import unittest
from main2 import Equipment


class MyTestCase(unittest.TestCase):
    def test_items_info(self):
        self.pila =  Equipment("Пила экста","зуб15","14.12.2024", 1200)
        self.test_string = "Номер = 1 название = Пила экста модель = зуб15 Дата покупки = 14.12.2024 цена = 1200"
        self.assertEqual(self.pila.__str__(), self.test_string)  # add assertion here


if __name__ == '__main__':
    unittest.main()
