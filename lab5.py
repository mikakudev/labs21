from datetime import datetime
_next = 0

def _next_number():
    global _next
    _next += 1
    return _next

#класс оборудования
class Equipment:
    def __init__(self,name = "default_name",model="default_model",purchase_date="000000",cost=0.00):
        self.__inventory_number = _next_number()
        self.__name = name
        self.__model = model
        self.__purchase_date = purchase_date
        self.__cost = cost
        self.time = datetime.now()
        with open('transaction.txt', 'a', encoding="utf-8") as f:
            f.write('Создали эквип №: {0}:{1}:{2}:{3}:{4} в {5} \n'.format(self.inventory_number,
                                                                           self.name,
                                                                           self.model,
                                                                           self.purchase_date,
                                                                           self.cost,
                                                                           self.time))
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

    @inventory_number.setter
    def inventory_number(self,num):
        if not isinstance(num, (int, float)):
            raise InvalidEquipmentNumberError()
        self.__inventory_number = num

    @cost.setter
    def cost(self,num):
        if not isinstance(num, (int, float)):
            raise InvalidEquipmentCostError()
        self.__cost = num



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

class InvalidEquipmentNumberError(Exception):
    def __init__(self, message="Номер оборудования должен быть числом"):
        self.message = message
        super().__init__(self.message)

class InvalidEquipmentCostError(Exception):
    def __init__(self, message="Cтоимость должна быть числом"):
        self.message = message
        super().__init__(self.message)

