from datetime import datetime
import pickle
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
        self.time = datetime.now()
        with open('transaction.txt', 'a', encoding="utf-8") as f:
            f.write('Создали эквип №: {0}:{1}:{2}:{3}:{4} в {5} \n'.format(self.inventory_number,
                                                                           self.name,
                                                                           self.model,
                                                                           self.purchase_date,
                                                                           self.cost,
                                                                           self.time))

    def __str__(self):
        return 'Номер = {0} название = {1} модель = {2} Дата покупки = {3} цена = {4}'.format(self.inventory_number,
                                                                                             self.name,
                                                                                             self.model,
                                                                                             self.purchase_date,
                                                                                             self.cost )

    def __del__(self):
        self.time = datetime.now()
        try:
            with open('transaction.txt', 'a', encoding="utf-8") as f:
                f.write('Удалили инвентарный номер: {0} в amount {1} \n'.format(self.inventory_number, self.time))
        except Exception as e:
            print(f"Ошибка при записи в лог при удалении Equipment: {e}")

#класс отдела
class Departament:
    def __init__(self,dep_number = 0 ,full_name = "Подразделение",short_name = "подразделение кратно",boss = "руководитель"):
        self.dep_number = dep_number
        self.full_name = full_name
        self.short_name = short_name
        self.boss = boss
        self.responsible_person = []
        self.rooms = []
        self.time = datetime.now()
        with open('transaction.txt', 'a', encoding="utf-8") as f:
            f.write('Создали Отдел №: {0}:{1}:{2}:{3}:{4} в {5} \n'.format(self.dep_number,
                                                                                    self.dep_number,
                                                                                    self.full_name,
                                                                                    self.short_name,
                                                                                    self.boss,
                                                                                    self.time))

    def __del__(self):
        self.time = datetime.now()
        try:
            with open('transaction.txt', 'a', encoding="utf-8") as f:
                f.write('Удалили отдел номер: {0} в amount {1} \n'.format(self.dep_number, self.time))
        except Exception as e:
            print(f"Ошибка при записи в лог при удалении Отдела: {e}")

class PickleEquip(object):
    @staticmethod
    def serialize(name):
           with open('equip.pkl', 'wb') as f:
               pickle.dump(name, f)

    @staticmethod
    def deserialize():
        with open('equip.pkl', 'rb') as f:
              pickle.load(f)

class PickleDep(object):
    @staticmethod
    def serialize(name):
        with open('dep.pkl', 'wb') as f:
            pickle.dump(name, f)

    @staticmethod
    def deserialize():
        with open('dep.pkl', 'rb') as f:
            pickle.load(f)


class ProEquip(Equipment):
    def __init__(self, name="default_name", model="default_model", purchase_date="000000", cost=0.00, vid="ВТ"):
        super(ProEquip, self).__init__( name, model, purchase_date, cost)
        self.vid = vid

    def __str__(self):
        return 'Номер = {0} название = {1} модель = {2} Дата покупки = {3} цена = {4} вид = {5}'.format(self.inventory_number,
                                                                                                              self.name,
                                                                                                              self.model,
                                                                                                              self.purchase_date,
                                                                                                              self.cost,
                                                                                                              self.vid)

        # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pila =  Equipment("Пила экста","зуб15","14.12.2024", 1200)

    dep = Departament(1,"Продажи", "СД", "Менеджер")
    print("номер", dep.dep_number, " наименование", dep.full_name, "кр. наим", dep.short_name, "руководитель", dep.boss)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
