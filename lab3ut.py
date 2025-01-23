import unittest
from main3 import Equipment
from main3 import PickleEquip


def read_last_line(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        if lines:
            return lines[-1].strip()
        else:
            return "Файл пуст"

# Использование:
last_line = read_last_line("transaction.txt")
print("Последняя строка файла:", last_line)

class check_trans(unittest.TestCase):
    def test_something(self):
        self.pila = Equipment("Пила экста", "зуб15", "14.12.2024", 1200)
        self.last_line = read_last_line("transaction.txt")
        if len(self.last_line) > 53:
            self.last_line = self.last_line[:51]
        self.str = "Создали эквип №: 1:Пила экста:зуб15:14.12.2024:1200"
        self.assertEqual(self.str, self.last_line)  # add assertion here

    def test_something2(self):
        self.pila = Equipment("Пила экста", "зуб15", "14.12.2024", 1200)
        self.do = self.pila.__str__()
        PickleEquip.serialize(self.pila)
        self.pila.__del__()
        PickleEquip.deserialize()
        self.posle = self.pila.__str__()
        self.assertEqual(self.do, self.posle)  # add assertion here

if __name__ == '__main__':
    unittest.main()
