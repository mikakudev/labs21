from datetime import datetime
import time

_next = 0

def _next_number():
    global _next
    _next += 1
    return _next

def time_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time of {func.__name__}: {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def count_calls(func):
    func.call_count = 0

    def wrapper(*args, **kwargs):
        func.call_count += 1
        print(f"{func.__name__} called {func.call_count} times")
        return func(*args, **kwargs)

    return wrapper

class Equipment:
    def __init__(self, name="default_name", model="default_model", purchase_date="000000", cost=0.00):
        self.__inventory_number = _next_number()
        self.__name = name
        self.__model = model
        self.__purchase_date = purchase_date
        self.__cost = cost
        self.__current_department = None
        self.__current_responsible = None
        self.__current_room = None
        self.__transfer_history = []
        self.time = datetime.now()
        with open('transaction.txt', 'a', encoding="utf-8") as f:
            f.write('Создали эквип №: {0}:{1}:{2}:{3}:{4} в {5} \n'.format(
                self.inventory_number, self.name, self.model, self.purchase_date, self.cost, self.time))

    @property
    def inventory_number(self):
        return self.__inventory_number

    @property
    def name(self):
        return self.__name

    @property
    def model(self):
        return self.__model

    @property
    def purchase_date(self):
        return self.__purchase_date

    @property
    def cost(self):
        return self.__cost

    @property
    def transfer_history(self):
        return self.__transfer_history

    @count_calls
    @time_execution
    def transfer(self, new_department=None, new_responsible=None, new_room=None):
        transfer_record = {
            "date": datetime.now(),
            "department": new_department.full_name if new_department else "Unknown",
            "responsible": new_responsible if new_responsible else "Unknown",
            "room": new_room.number if new_room else "Unknown"
        }
        self.__transfer_history.append(transfer_record)
        self.__current_department = new_department
        self.__current_responsible = new_responsible
        self.__current_room = new_room

    def __repr__(self):
        return f"{self.name} (#{self.inventory_number}, Model: {self.model})"

class Room:
    def __init__(self, number, area):
        self.number = number
        self.area = area
        self.equipment = []

    @count_calls
    @time_execution
    def add_equipment(self, equipment, department):
        self.equipment.append(equipment)
        equipment.transfer(new_department=department, new_responsible=None, new_room=self)

    def __repr__(self):
        return f"Room {self.number} ({self.area} sq.m) with equipment: {self.equipment}"

class Departament:
    def __init__(self, dep_number=0, full_name="Подразделение", short_name="подразделение кратно", boss="руководитель"):
        self.dep_number = dep_number
        self.full_name = full_name
        self.short_name = short_name
        self.boss = boss
        self.responsible_persons = []
        self.rooms = []
        self.time = datetime.now()
        with open('transaction.txt', 'a', encoding="utf-8") as f:
            f.write('Создали Отдел №: {0}:{1}:{2}:{3}:{4} в {5} \n'.format(self.dep_number,
                                                                           self.dep_number,
                                                                           self.full_name,
                                                                           self.short_name,
                                                                           self.boss,
                                                                           self.time))

    @count_calls
    @time_execution
    def add_room(self, room):
        self.rooms.append(room)

    @count_calls
    @time_execution
    def add_responsible_person(self, person):
        self.responsible_persons.append(person)

    @count_calls
    @time_execution
    def list_equipment(self):
        equipment_list = []
        for room in self.rooms:
            equipment_list.extend(room.equipment)
        return equipment_list

    def __del__(self):
        self.time = datetime.now()
        try:
            with open('transaction.txt', 'a', encoding="utf-8") as f:
                f.write('Удалили отдел номер: {0} в amount {1} \n'.format(self.dep_number, self.time))
        except Exception as e:
            print(f"Ошибка при записи в лог при удалении Отдела: {e}")

class Company:
    def __init__(self, name):
        self.__company_name = name
        self.departments = []

    @count_calls
    @time_execution
    def add_department(self, department):
        self.departments.append(department)

    @count_calls
    @time_execution
    def list_all_equipment(self):
        all_equipment = []
        for department in self.departments:
            all_equipment.extend(department.list_equipment())
        return all_equipment

    def __repr__(self):
        return f"Company: {self.__company_name}, Departments: {len(self.departments)}"

class InvalidEquipmentNumberError(Exception):
    def __init__(self, message="Номер оборудования должен быть числом"):
        self.message = message
        super().__init__(self.message)

class InvalidEquipmentCostError(Exception):
    def __init__(self, message="Cтоимость должна быть числом"):
        self.message = message
        super().__init__(self.message)

# Example usage
def main():
    company = Company("Tech Enterprise")

    # Create departments
    it_department = Departament(1, "IT Department", "IT", "Alice Smith")
    finance_department = Departament(2, "Finance Department", "Finance", "Bob Johnson")

    # Create rooms
    it_room = Room(101, 50)
    finance_room = Room(201, 40)

    it_department.add_room(it_room)
    finance_department.add_room(finance_room)

    # Create equipment
    laptop = Equipment("Laptop", "Dell XPS 15", "2023-01-15", 1500.00)
    printer = Equipment("Printer", "HP LaserJet", "2022-12-20", 300.00)

    it_room.add_equipment(laptop, it_department)
    finance_room.add_equipment(printer, finance_department)

    # Add departments to company
    company.add_department(it_department)
    company.add_department(finance_department)

    print(company)
    print("IT Department Rooms and Equipment:")
    for room in it_department.rooms:
        print(room)

    print("Finance Department Rooms and Equipment:")
    for room in finance_department.rooms:
        print(room)

if __name__ == "__main__":
    main()
