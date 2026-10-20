# Лабораторная работа 5, задание 1. Дробь (Fraction)
from math import gcd
from functools import total_ordering


# Декоратор автоматически добавляет остальные операции сравнения
# на основе методов __eq__ и __lt__
@total_ordering
class Fraction:
    def __init__(self, top, bottom=1):
        # Проверяем, что знаменатель не равен нулю
        if bottom == 0:
            raise ValueError('Знаменатель не может быть равен нулю')

        # Если знаменатель отрицательный, переносим знак в числитель
        if bottom < 0:
            top, bottom = -top, -bottom

        # Сокращаем дробь с помощью НОД
        d = gcd(abs(top), bottom) or 1
        self.top, self.bottom = top // d, bottom // d

    # Сложение двух дробей
    def __add__(self, o):
        return Fraction(self.top * o.bottom + o.top * self.bottom, self.bottom * o.bottom)

    # Вычитание двух дробей
    def __sub__(self, o):
        return Fraction(self.top * o.bottom - o.top * self.bottom, self.bottom * o.bottom)

    # Умножение двух дробей
    def __mul__(self, o):
        return Fraction(self.top * o.top, self.bottom * o.bottom)

    # Деление двух дробей
    def __truediv__(self, o):
        return Fraction(self.top * o.bottom, self.bottom * o.top)

    # Изменение знака дроби на противоположный
    def __neg__(self):
        return Fraction(-self.top, self.bottom)

    # Возвращаем абсолютное значение дроби
    def __abs__(self):
        return Fraction(abs(self.top), self.bottom)

    # Проверяем равенство дробей
    def __eq__(self, o):
        return self.top == o.top and self.bottom == o.bottom

    # Сравниваем дроби без перевода в десятичные числа
    def __lt__(self, o):
        return self.top * o.bottom < o.top * self.bottom

    # Позволяет использовать дроби в множествах и словарях
    def __hash__(self):
        return hash((self.top, self.bottom))

    # Преобразуем дробь в десятичное число
    def __float__(self):
        return self.top / self.bottom

    # Преобразуем дробь в целое число, отбрасывая дробную часть
    def __int__(self):
        return int(float(self))

    # Определяем, как дробь отображается через print()
    def __str__(self):
        return f'{self.top}/{self.bottom}'

    # Определяем представление объекта для отладки
    def __repr__(self):
        return f'Fraction({self.top}, {self.bottom})'


# Создаём две дроби
p, q = Fraction(2, 3), Fraction(1, 4)
print('p =', p, '| q =', q, '| repr:', repr(p))

# Проверяем арифметические операции
print('p + q =', p + q, '| p - q =', p - q, '| p * q =', p * q, '| p / q =', p / q)

# Проверяем смену знака, модуль и сокращение дроби
print('-p =', -p, '| abs(-p) =', abs(-p), '| Fraction(6, -8) =', Fraction(6, -8))

# Проверяем операции сравнения
print('p > q:', p > q, '| p <= q:', p <= q, '| p == Fraction(4, 6):', p == Fraction(4, 6))

# Проверяем преобразование дроби в float и int
print('float(p) =', round(float(p), 4), '| int(Fraction(7, 2)) =', int(Fraction(7, 2)))

# Выполняем несколько операций с дробями в одном выражении
result = (Fraction(2, 3) + Fraction(1, 4)) * Fraction(6, 7) - Fraction(1, 12)
print('(2/3 + 1/4) * 6/7 - 1/12 =', result)

# Проверяем обработку ошибки при нулевом знаменателе
try:
    Fraction(3, 0)
except ValueError as err:
    print('Ошибка:', err)