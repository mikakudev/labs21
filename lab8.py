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
        print(f"Время выполнения {func.__name__}: {end_time - start_time:.4f} секунд")
        return result
    return wrapper

def count_calls(func):
    func.call_count = 0

    def wrapper(*args, **kwargs):
        func.call_count += 1
        print(f"{func.__name__} вызвано {func.call_count} раз(а)")
        return func(*args, **kwargs)

    return wrapper

class Equipment:
    def __init__(self, name="по умолчанию", model="по умолчанию", purchase_date="000000", cost=0.00):
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
            f.write('Создано оборудование №: {0}:{1}:{2}:{3}:{4} в {5} \n'.format(
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
            "дата": datetime.now(),
            "отдел": new_department.full_name if new_department else "Неизвестно",
            "ответственный": new_responsible if new_responsible else "Неизвестно",
            "комната": new_room.number if new_room else "Неизвестно"
        }
        self.__transfer_history.append(transfer_record)
        self.__current_department = new_department
        self.__current_responsible = new_responsible
        self.__current_room = new_room

    def __repr__(self):
        return f"{self.name} (№{self.inventory_number}, Модель: {self.model})"

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
        return f"Комната {self.number} ({self.area} кв.м) с оборудованием: {self.equipment}"

class Departament:
    def __init__(self, dep_number=0, full_name="Подразделение", short_name="подразделение кратко", boss="руководитель"):
        self.dep_number = dep_number
        self.full_name = full_name
        self.short_name = short_name
        self.boss = boss
        self.responsible_persons = []
        self.rooms = []
        self.time = datetime.now()
        with open('transaction.txt', 'a', encoding="utf-8") as f:
            f.write('Создан Отдел №: {0}:{1}:{2}:{3}:{4} в {5} \n'.format(self.dep_number,
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
                f.write('Удален Отдел №: {0} в {1} \n'.format(self.dep_number, self.time))
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
        return f"Компания: {self.__company_name}, Отделов: {len(self.departments)}"

class InvalidEquipmentNumberError(Exception):
    def __init__(self, message="Номер оборудования должен быть числом"):
        self.message = message
        super().__init__(self.message)

class InvalidEquipmentCostError(Exception):
    def __init__(self, message="Cтоимость должна быть числом"):
        self.message = message
        super().__init__(self.message)

def main():
    print("Добро пожаловать в систему учета компании!")

    company = Company("Техническое предприятие")

    while True:
        print("\nВыберите действие:")
        print("1. Создать отдел")
        print("2. Создать комнату в отделе")
        print("3. Добавить оборудование в комнату")
        print("4. Показать информацию о компании")
        print("5. Выйти")

        choice = input("Введите номер действия: ")

        if choice == "1":
            dep_number = int(input("Введите номер отдела: "))
            full_name = input("Введите полное название отдела: ")
            short_name = input("Введите краткое название отдела: ")
            boss = input("Введите имя руководителя отдела: ")
            department = Departament(dep_number, full_name, short_name, boss)
            company.add_department(department)
            print(f"Отдел '{full_name}' создан.")

        elif choice == "2":
            dep_number = int(input("Введите номер отдела, в который хотите добавить комнату: "))
            department = next((d for d in company.departments if d.dep_number == dep_number), None)
            if not department:
                print("Отдел с таким номером не найден.")
                continue
            room_number = int(input("Введите номер комнаты: "))
            room_area = float(input("Введите площадь комнаты (кв.м): "))
            room = Room(room_number, room_area)
            department.add_room(room)
            print(f"Комната {room_number} добавлена в отдел '{department.full_name}'.")

        elif choice == "3":
            dep_number = int(input("Введите номер отдела, где находится комната: "))
            department = next((d for d in company.departments if d.dep_number == dep_number), None)
            if not department:
                print("Отдел с таким номером не найден.")
                continue
            room_number = int(input("Введите номер комнаты, куда добавить оборудование: "))
            room = next((r for r in department.rooms if r.number == room_number), None)
            if not room:
                print("Комната с таким номером не найдена.")
                continue
            name = input("Введите название оборудования: ")
            model = input("Введите модель оборудования: ")
            purchase_date = input("Введите дату покупки оборудования (ГГГГ-ММ-ДД): ")
            cost = float(input("Введите стоимость оборудования: "))
            equipment = Equipment(name, model, purchase_date, cost)
            room.add_equipment(equipment, department)
            print(f"Оборудование '{name}' добавлено в комнату {room_number}.")

        elif choice == "4":
            print(company)
            for department in company.departments:
                print(f"\nОтдел: {department.full_name}")
                print("Комнаты:")
                for room in department.rooms:
                    print(room)
                print("Ответственные лица:", department.responsible_persons)

        elif choice == "5":
            print("Выход из программы. До свидания!")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
