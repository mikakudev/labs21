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
    def __init__(self, name="по умолчанию", model="по умолчанию", purchase_date="0000-00-00", cost=0.00):
        self.__inventory_number = _next_number()
        self.__name = name
        self.__model = model
        self.__purchase_date = purchase_date
        self.__cost = cost
        self.__current_department = None
        self.__current_responsible = None
        self.__current_room = None
        self.__transfer_history = []

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
            "ответственный": f"{new_responsible['ФИО']} ({new_responsible['должность']})" if new_responsible else "Неизвестно",
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
    def add_equipment(self, equipment, department, responsible):
        self.equipment.append(equipment)
        equipment.transfer(new_department=department, new_responsible=responsible, new_room=self)

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

    @count_calls
    @time_execution
    def list_rooms(self):
        return self.rooms

    def __repr__(self):
        return f"Отдел {self.full_name} ({self.dep_number})"

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

    def list_equipment_by_responsible(self, responsible_name):
        result = []
        for department in self.departments:
            for room in department.rooms:
                for equipment in room.equipment:
                    if equipment._Equipment__current_responsible and equipment._Equipment__current_responsible["ФИО"] == responsible_name:
                        result.append(equipment)
        return result

    def __repr__(self):
        return f"Компания: {self.__company_name}, Отделов: {len(self.departments)}"

# Пример использования

def main():
    print("Добро пожаловать в систему учета компании!")

    company = Company("Техническое предприятие")

    while True:
        print("\nМеню:")
        print("1. Создать отдел")
        print("2. Добавить комнату в отдел")
        print("3. Добавить оборудование в комнату")
        print("4. Указать материально ответственное лицо")
        print("5. Передать оборудование")
        print("6. Вывести список оборудования в компании")
        print("7. Вывести список помещений отдела")
        print("8. Показать оборудование по ответственному лицу")
        print("9. Выйти")

        choice = input("Введите номер действия: ")

        if choice == "1":
            dep_number = int(input("Введите номер отдела: "))
            full_name = input("Введите полное название отдела: ")
            short_name = input("Введите краткое название отдела: ")
            boss = input("Введите имя руководителя отдела: ")
            department = Departament(dep_number, full_name, short_name, boss)
            company.add_department(department)
            print("Отдел создан.")

        elif choice == "2":
            dep_number = int(input("Введите номер отдела: "))
            department = next((d for d in company.departments if d.dep_number == dep_number), None)
            if department:
                room_number = input("Введите номер комнаты: ")
                room_area = float(input("Введите площадь комнаты: "))
                room = Room(room_number, room_area)
                department.add_room(room)
                print("Комната добавлена.")
            else:
                print("Отдел не найден.")

        elif choice == "3":
            dep_number = int(input("Введите номер отдела: "))
            department = next((d for d in company.departments if d.dep_number == dep_number), None)
            if department:
                room_number = input("Введите номер комнаты: ")
                room = next((r for r in department.rooms if r.number == room_number), None)
                if room:
                    name = input("Введите название оборудования: ")
                    model = input("Введите модель оборудования: ")
                    purchase_date = input("Введите дату покупки (гггг-мм-дд): ")
                    cost = float(input("Введите стоимость оборудования: "))
                    equipment = Equipment(name, model, purchase_date, cost)
                    responsible_name = input("Введите имя материально ответственного лица: ")
                    responsible = next((p for p in department.responsible_persons if p["ФИО"] == responsible_name), None)
                    if responsible:
                        room.add_equipment(equipment, department, responsible)
                        print("Оборудование добавлено в комнату.")
                    else:
                        print("Материально ответственное лицо не найдено.")
                else:
                    print("Комната не найдена.")
            else:
                print("Отдел не найден.")

        elif choice == "4":
            dep_number = int(input("Введите номер отдела: "))
            department = next((d for d in company.departments if d.dep_number == dep_number), None)
            if department:
                name = input("Введите имя материально ответственного лица: ")
                position = input("Введите должность материально ответственого лица: ")
                responsible = {"ФИО": name, "должность": position}
                department.add_responsible_person(responsible)
                print("Материально ответственное лицо добавлено.")
            else:
                print("Отдел не найден.")

        elif choice == "5":
            inventory_number = int(input("Введите инвентарный номер оборудования: "))
            new_dep_number = int(input("Введите номер нового отдела: "))
            new_department = next((d for d in company.departments if d.dep_number == new_dep_number), None)
            if new_department:
                room_number = input("Введите номер новой комнаты: ")
                new_room = next((r for r in new_department.rooms if r.number == room_number), None)
                responsible_name = input("Введите имя нового материально ответственного лица: ")
                new_responsible = next((p for p in new_department.responsible_persons if p["ФИО"] == responsible_name), None)

                if new_room and new_responsible:
                    equipment = None
                    for d in company.departments:
                        for r in d.rooms:
                            equipment = next((e for e in r.equipment if e.inventory_number == inventory_number), None)
                            if equipment:
                                r.equipment.remove(equipment)
                                break
                        if equipment:
                            break

                    if equipment:
                        equipment.transfer(new_department=new_department, new_responsible=new_responsible, new_room=new_room)
                        new_room.add_equipment(equipment, new_department, new_responsible)
                        print("Оборудование успешно передано.")
                    else:
                        print("Оборудование с таким инвентарным номером не найдено.")
                else:
                    print("Комната или материально ответственное лицо не найдены.")
            else:
                print("Отдел не найден.")

        elif choice == "6":
            all_equipment = company.list_all_equipment()
            print("Список оборудования в компании:")
            for equipment in all_equipment:
                print(equipment)

        elif choice == "7":
            dep_number = int(input("Введите номер отдела: "))
            department = next((d for d in company.departments if d.dep_number == dep_number), None)
            if department:
                print("Список помещений отдела:")
                for room in department.list_rooms():
                    print(f"Комната {room.number}, Площадь: {room.area} кв.м")
            else:
                print("Отдел не найден.")

        elif choice == "8":
            responsible_name = input("Введите имя материально ответственного лица: ")
            responsible_equipment = company.list_equipment_by_responsible(responsible_name)
            if responsible_equipment:
                print(f"Оборудование у {responsible_name}:")
                for equipment in responsible_equipment:
                    print(equipment)
            else:
                print("Указанное лицо не имеет закрепленного оборудования.")
        elif choice == "9":
          print("Выход из программы. До свидания!")
          break

        else:
          print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()