# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

_next = 0

def _next_number():
    global _next
    _next += 1
    return _next


#класс оборудования
class Equipment:
    def __init__(self,name = "default_name",model="default_model",purchase_date="000000",cost=0.00):
        self.inventory_number = _next_number()
        self.name = name
        self.model = model
        self.purchase_date = purchase_date
        self.cost = cost

    def __str__(self):
        return 'Номер = {0} название = {1} модель = {2} Дата покупки = {3} цена = {4}'.format(self.inventory_number,
                                                                                             self.name,
                                                                                             self.model,
                                                                                             self.purchase_date,
                                                                                             self.cost )


#класс отдела
class Departament:
    def __init__(self,dep_number = 0 ,full_name = "Подлазделение",short_name = "подразделение кратно",boss = "руководитель"):
        self.dep_number = dep_number
        self.full_name = full_name
        self.short_name = short_name
        self.boss = boss
        self.responsible_person = []
        self.rooms = []


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
 drel = Equipment("1","дрель рысь","Гд70","14.12.2024", 1200)
 print("инвентарный № ",drel.inventory_number, " наименование ",drel.name ,
       " Модель", drel.model, "дата покупки ", drel.purchase_date, "стоимость", drel.cost)

 dep = Departament("1","Продажи", "СД", "Менеджер")
 print("номер", dep.dep_number, " наименование", dep.full_name, "кр. наим", dep.short_name, "руководитель", dep.boss)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
