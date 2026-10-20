# Лабораторная работа 5, задание 6. Деньги (Money)
from decimal import Decimal, ROUND_HALF_UP
from functools import total_ordering


# Декоратор автоматически добавляет остальные операции сравнения
@total_ordering
class Money:
    def __init__(self, value, cur='KGS'):
        # Преобразуем сумму в Decimal и округляем до двух знаков
        self.value = Decimal(str(value)).quantize(Decimal('0.01'), ROUND_HALF_UP)
        self.cur = cur  # Валюта: KGS, USD и т. д.

    # Проверяем, совпадают ли валюты двух денежных значений
    def _check(self, o):
        if self.cur != o.cur:
            raise ValueError(f'Разные валюты: {self.cur} и {o.cur}')

    # Сложение денежных сумм
    def __add__(self, o): self._check(o); return Money(self.value + o.value, self.cur)

    # Вычитание денежных сумм
    def __sub__(self, o): self._check(o); return Money(self.value - o.value, self.cur)

    # Умножение суммы на число
    def __mul__(self, k): return Money(self.value * Decimal(str(k)), self.cur)

    # Деление суммы на число
    def __truediv__(self, k): return Money(self.value / Decimal(str(k)), self.cur)

    # Проверяем равенство сумм и валют
    def __eq__(self, o): return self.cur == o.cur and self.value == o.value

    # Сравниваем суммы в одной валюте
    def __lt__(self, o): self._check(o); return self.value < o.value

    # Возвращаем абсолютное значение суммы
    def __abs__(self): return Money(abs(self.value), self.cur)

    # Проверяем, не равна ли сумма нулю
    def __bool__(self): return self.value != 0

    # Округляем сумму до указанного количества знаков
    def __round__(self, n=0): return Money(round(self.value, n), self.cur)

    # Строковое представление суммы
    def __str__(self): return f'{self.value} {self.cur}'

    # Представление объекта для отладки
    def __repr__(self): return f"Money('{self.value}', '{self.cur}')"

    # Переводим сумму в другую валюту по заданному курсу
    def convert(self, rate, new_cur):
        return Money(self.value * Decimal(str(rate)), new_cur)


# Создаём денежные значения для разных расходов
rent, food, net = Money(18500), Money('9240.50'), Money(1250.75)
print('rent =', rent, '| repr:', repr(food))

# Проверяем сложение и вычитание денежных сумм
print('rent + food =', rent + food, '| rent - food =', rent - food)

# Проверяем умножение, деление и округление
print('net * 3 =', net * 3, '| food / 4 =', food / 4, '| round(food / 7) =', round(food / 7))

# Проверяем сравнение, модуль отрицательной суммы и логическое значение нуля
print('rent > food:', rent > food, '| abs(Money(-40)) =', abs(Money(-40)), '| bool(Money(0)) =', bool(Money(0)))

# Переводим сумму из сомов в доллары по заданному курсу
print('net в долларах (курс 0.0114):', net.convert('0.0114', 'USD'))

# Проверяем, что нельзя складывать суммы в разных валютах
try:
    rent + Money(10, 'USD')
except ValueError as err:
    print('Ошибка:', err)

# Формируем список расходов
budget = [('Аренда', rent), ('Питание', food), ('Интернет', net), ('Транспорт', Money(3100))]
total = Money(0)  # Начальная общая сумма расходов

# Выводим каждый расход и рассчитываем общую сумму
for title, cost in budget:
    print(f'{title:<10}{cost.value:>10}')
    total = total + cost

# Выводим итоговую сумму и сумму с резервом 10%
print('Смета, итого:', total, '| с резервом 10%:', total * '1.1')