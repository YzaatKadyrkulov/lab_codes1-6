# Лабораторная работа 5, задание 7. Числовой интервал (Interval)


# Класс для работы с числовыми интервалами
class Interval:
    def __init__(self, left, right):
        # Проверяем, что начало интервала не больше конца
        if left > right:
            raise ValueError('Начало интервала больше конца')
        self.left, self.right = left, right  # Левая и правая границы

    # Проверяем, входит ли число в интервал
    def __contains__(self, x): return self.left <= x <= self.right

    # Находим пересечение двух интервалов
    def __and__(self, o):
        lo, hi = max(self.left, o.left), min(self.right, o.right)
        return Interval(lo, hi) if lo <= hi else None

    # Создаём общий интервал от минимальной до максимальной границы
    def __or__(self, o): return Interval(min(self.left, o.left), max(self.right, o.right))

    # Сдвигаем интервал на заданное число
    def __add__(self, shift): return Interval(self.left + shift, self.right + shift)

    # Возвращаем целую часть длины интервала
    def __len__(self): return int(self.right - self.left)

    # Проверяем равенство границ двух интервалов
    def __eq__(self, o): return (self.left, self.right) == (o.left, o.right)

    # Проверяем, имеет ли интервал ненулевую целую длину
    def __bool__(self): return len(self) != 0

    # Строковое представление интервала
    def __str__(self): return f'[{self.left}, {self.right}]'

    # Представление объекта для отладки
    def __repr__(self): return f'Interval({self.left}, {self.right})'

    # Проверяем, пересекаются ли два интервала
    def overlaps(self, o): return (self & o) is not None

    # Делим интервал на n равных частей
    def split(self, n):
        step = (self.right - self.left) / n
        return [Interval(self.left + i * step, self.left + (i + 1) * step) for i in range(n)]


# Создаём три интервала
a, b, c = Interval(2, 9), Interval(6, 15), Interval(20, 25)
print('a =', a, '| b =', b, '| c =', c, '| repr:', repr(a))

# Проверяем, входят ли числа в интервал a
print('5 in a:', 5 in a, '| 12 in a:', 12 in a)

# Проверяем пересечение интервалов
print('a & b =', a & b, '| a & c =', a & c)

# Проверяем объединение интервалов и сдвиг на 10
print('a | c =', a | c, '| a + 10 =', a + 10)

# Проверяем длину и логическое значение интервала
print('len(a) =', len(a), '| bool(Interval(4, 4)) =', bool(Interval(4, 4)))

# Проверяем равенство интервалов и наличие пересечения
print('a == Interval(2, 9):', a == Interval(2, 9), '| a.overlaps(b):', a.overlaps(b), '| a.overlaps(c):', a.overlaps(c))

# Разбиваем интервал a на 7 равных частей
print('a.split(7):', ', '.join(str(p) for p in a.split(7)))

# Проверяем обработку ошибки при неправильных границах
try:
    Interval(8, 3)
except ValueError as err:
    print('Ошибка:', err)