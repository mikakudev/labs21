# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from datetime import date
#класс оборудования
class Equipment:
    def __init__(self,inventory_number,name,model,purchase_date,cost):
        self.inventory_number = inventory_number
        self.name = name
        self.model = model
        self.purchase_date = purchase_date
        self.cost = cost


#класс отдела
class Departament:
    def __init__(self,dep_number,full_name,short_name,boss):
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
