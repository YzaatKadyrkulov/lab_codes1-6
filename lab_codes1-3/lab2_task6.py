# Лабораторная работа 2, задание 6. Класс «Тарифный план»
class TariffPlan:
    def __init__(self, label, cost, mbit, talk, texts):
        # приватные атрибуты (name mangling): снаружи класса напрямую недоступны
        self.__label = label
        # присваивание идёт через сеттер, поэтому проверка цены работает
        # уже при создании объекта
        self.price = cost
        self.__mbit = mbit                 # скорость интернета, Мбит/с
        self.__talk = talk                 # включённые минуты
        self.__texts = texts               # включённые SMS

    # геттер: вызывается при чтении plan.price
    @property
    def price(self):
        return self.__price

    # сеттер: цена должна быть положительной
    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError('Цена должна быть больше нуля')
        self.__price = value

    # название только для чтения: сеттера нет
    @property
    def label(self):
        return self.__label

    # вычисляемое свойство: «ценность» тарифа на один сом (не хранится в объекте);
    # минуты и SMS учитываются с понижающими коэффициентами 1/10 и 1/20
    @property
    def value_index(self):
        return round((self.__mbit + self.__talk / 10 + self.__texts / 20) / self.__price, 3)

    # стоимость за год = цена в месяц × 12
    def annual_cost(self):
        return self.__price * 12

    # цена со скидкой в процентах
    def discount_price(self, percent):
        return round(self.__price * (1 - percent / 100), 2)

    # сравниваем два тарифа по цене и по «ценности»
    # (other.__price допустим: внутри класса доступ к приватному атрибуту другого
    # объекта того же класса разрешён)
    def compare(self, other):
        cheaper = self if self.__price < other.__price else other
        better = self if self.value_index > other.value_index else other
        return f'дешевле «{cheaper.label}», выгоднее «{better.label}»'

    # строка для print(): основные характеристики тарифа
    def __str__(self):
        return (f'{self.__label}: {self.__price} сом/мес, {self.__mbit} Мбит/с, '
                f'{self.__talk} мин, {self.__texts} SMS')


# создаём четыре тарифа для сравнения
plans = [
    TariffPlan('Старт', 350, 20, 200, 50),
    TariffPlan('Оптимум', 590, 60, 600, 200),
    TariffPlan('Безлимит', 890, 150, 1500, 500),
    TariffPlan('Студент', 290, 30, 300, 100),
]
for p in plans:
    print(p, f'| год: {p.annual_cost()} | -15%: {p.discount_price(15)} | ценность {p.value_index}')
print('Сравнение:', plans[0].compare(plans[3]))

# оптимальный тариф — с наибольшей «ценностью» (max с lambda-ключом)
print('Оптимальный тариф:', max(plans, key=lambda p: p.value_index).label)

# проверяем валидацию: неположительная цена вызывает ValueError
try:
    plans[0].price = -50
except ValueError as err:
    print('Ошибка:', err)