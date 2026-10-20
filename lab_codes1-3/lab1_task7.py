# Лабораторная работа 1, задание 7. Класс «Смартфон»
class Smartphone:
    # конструктор: вызывается автоматически при создании объекта
    def __init__(self, maker, version, ram, battery, released, cost):
        # атрибуты экземпляра: у каждого смартфона свои значения
        self.maker = maker                 # бренд
        self.version = version             # модель
        self.ram = ram                     # ОЗУ, ГБ
        self.battery = battery             # ёмкость, мАч
        self.released = released           # год выхода
        self.cost = cost                   # цена, $

    # собираем описание из атрибутов конкретного объекта (self)
    def describe(self):
        return (f'{self.maker} {self.version} ({self.released}): '
                f'{self.ram} ГБ ОЗУ, {self.battery} мАч, ${self.cost}')

    # флагман — смартфон с ОЗУ не меньше min_ram (параметр по умолчанию 8 ГБ)
    def is_flagship(self, min_ram=8):
        return self.ram >= min_ram

    # на сколько суток хватит заряда при заданном суточном расходе
    def battery_days(self, usage_mah_per_day):
        return round(self.battery / usage_mah_per_day, 1)


# создаём четыре объекта одного класса (разные бренды)
phones = [
    Smartphone('Samsung', 'Galaxy A55', 8, 5000, 2024, 450),
    Smartphone('Xiaomi', 'Redmi Note 13', 6, 5000, 2024, 230),
    Smartphone('Honor', 'Magic6 Lite', 8, 5300, 2024, 380),
    Smartphone('Nokia', 'G42', 4, 5000, 2023, 190),
]

# вызываем методы у каждого объекта в цикле
for ph in phones:
    print(ph.describe())
    # расход 2200 мАч в сутки передаём в метод как аргумент
    print(f'флагман: {ph.is_flagship()}, '
          f'без зарядки при 2200 мАч/сутки: {ph.battery_days(2200)} дн.')