import unittest
from datetime import datetime
from labbb8 import Equipment, Room, Departament, Company

class TestEquipmentManagement(unittest.TestCase):
    def test_equipment_creation(self):
        eq = Equipment(name="Printer", model="HP1234", purchase_date="2025-01-01", cost=500.0)
        self.assertEqual(eq.name, "Printer")
        self.assertEqual(eq.model, "HP1234")
        self.assertEqual(eq.purchase_date, "2025-01-01")
        self.assertEqual(eq.cost, 500.0)

    def test_transfer_equipment(self):
        eq = Equipment(name="Printer")
        dep = Departament(full_name="IT Department")
        room = Room(number=101, area=50)
        responsible = {"ФИО": "John Doe", "должность": "Engineer"}

        eq.transfer(new_department=dep, new_responsible=responsible, new_room=room)

        self.assertEqual(eq._Equipment__current_department, dep)
        self.assertEqual(eq._Equipment__current_responsible, responsible)
        self.assertEqual(eq._Equipment__current_room, room)

    def test_room_add_equipment(self):
        eq = Equipment(name="Monitor")
        dep = Departament(full_name="HR Department")
        room = Room(number=102, area=30)
        responsible = {"ФИО": "Jane Smith", "должность": "Manager"}

        room.add_equipment(eq, department=dep, responsible=responsible)

        self.assertIn(eq, room.equipment)
        self.assertEqual(eq._Equipment__current_room, room)

    def test_department_list_equipment(self):
        dep = Departament(full_name="Finance")
        room1 = Room(number=201, area=40)
        room2 = Room(number=202, area=35)
        eq1 = Equipment(name="Laptop")
        eq2 = Equipment(name="Projector")

        dep.add_room(room1)
        dep.add_room(room2)
        room1.add_equipment(eq1, department=dep, responsible={"ФИО": "Alice", "должность": "Analyst"})
        room2.add_equipment(eq2, department=dep, responsible={"ФИО": "Bob", "должность": "Clerk"})

        equipment_list = dep.list_equipment()

        self.assertIn(eq1, equipment_list)
        self.assertIn(eq2, equipment_list)

    def test_company_add_department(self):
        company = Company(name="TechCorp")
        dep = Departament(full_name="R&D")

        company.add_department(dep)

        self.assertIn(dep, company.departments)

    def test_company_list_all_equipment(self):
        company = Company(name="TechCorp")
        dep = Departament(full_name="Logistics")
        room = Room(number=301, area=60)
        eq = Equipment(name="Forklift")

        dep.add_room(room)
        room.add_equipment(eq, department=dep, responsible={"ФИО": "Charlie", "должность": "Operator"})
        company.add_department(dep)

        all_equipment = company.list_all_equipment()

        self.assertIn(eq, all_equipment)

if __name__ == "__main__":
    unittest.main()