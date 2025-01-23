import unittest
from lab5 import Equipment, InvalidEquipmentNumberError, InvalidEquipmentCostError  # Предполагается, что код сохранен в файле equipment.py

class TestEquipment(unittest.TestCase):

    def test_invalid_inventory_number(self):
        equipment = Equipment()
        with self.assertRaises(InvalidEquipmentNumberError) as context:
            equipment.inventory_number = "InvalidNumber"  # Некорректное значение для inventory_number
        self.assertEqual(str(context.exception), "Номер оборудования должен быть числом")

    def test_invalid_cost(self):
        equipment = Equipment()
        with self.assertRaises(InvalidEquipmentCostError) as context:
            equipment.cost = "InvalidCost"  # Некорректное значение для cost
        self.assertEqual(str(context.exception), "Cтоимость должна быть числом")

    def test_valid_inventory_number_and_cost(self):
        equipment = Equipment()
        try:
            equipment.inventory_number = 100  # Корректное значение для inventory_number
            equipment.cost = 250.75  # Корректное значение для cost
        except (InvalidEquipmentNumberError, InvalidEquipmentCostError):
            self.fail("Unexpected exception raised for valid inputs!")

if __name__ == "__main__":
    unittest.main()