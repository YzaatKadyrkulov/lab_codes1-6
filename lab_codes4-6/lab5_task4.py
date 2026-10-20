# Лабораторная работа 5, задание 4. Набор точек (PointSet)
import math


# Класс для представления точки на плоскости
class Point:
    def __init__(self, px, py):
        self.px, self.py = px, py  # Координаты точки x и y

    # Строковое представление точки
    def __str__(self): return f'({self.px}; {self.py})'

    # Представление объекта для отладки
    def __repr__(self): return f'Point({self.px}, {self.py})'

    # Проверка равенства двух точек
    def __eq__(self, o): return self.px == o.px and self.py == o.py

    # Позволяет использовать точки в множествах и словарях
    def __hash__(self): return hash((self.px, self.py))

    # Сложение координат двух точек
    def __add__(self, o): return Point(self.px + o.px, self.py + o.py)

    # Вычитание координат двух точек
    def __sub__(self, o): return Point(self.px - o.px, self.py - o.py)

    # Расстояние от начала координат до точки
    def __abs__(self): return math.hypot(self.px, self.py)

    # Расстояние между двумя точками
    def distance_to(self, o): return abs(self - o)


# Класс для хранения и обработки набора точек
class PointSet:
    def __init__(self, items=()):
        self.items = list(items)  # Сохраняем точки в списке

    # Количество точек в наборе
    def __len__(self): return len(self.items)

    # Получение точки по индексу
    def __getitem__(self, i): return self.items[i]

    # Замена точки по индексу
    def __setitem__(self, i, v): self.items[i] = v

    # Проверка наличия точки в наборе
    def __contains__(self, p): return p in self.items

    # Объединение двух наборов точек
    def __add__(self, o): return PointSet(self.items + o.items)

    # Позволяет перебирать точки циклом for
    def __iter__(self): return iter(self.items)

    # Преобразование набора точек в строку
    def __str__(self): return '{' + ', '.join(str(p) for p in self.items) + '}'

    # Вычисление центра масс набора точек
    def centroid(self):
        n = len(self)
        return Point(round(sum(p.px for p in self) / n, 2), round(sum(p.py for p in self) / n, 2))

    # Поиск точки, ближайшей к заданной
    def nearest_to(self, pt):
        return min(self.items, key=lambda p: p.distance_to(pt))

    # Поиск границ прямоугольника, содержащего все точки
    def bounding_box(self):
        xs, ys = [p.px for p in self], [p.py for p in self]
        return Point(min(xs), min(ys)), Point(max(xs), max(ys))


# Создаём два набора точек
A = PointSet([Point(1, 2), Point(4, 6), Point(-3, 5)])
B = PointSet([Point(7, -1), Point(0, 0)])

# Выводим набор, количество точек, точку по индексу и repr()
print('A =', A, '| len(A) =', len(A), '| A[1] =', A[1], '| repr:', repr(A[0]))

# Проверяем, содержатся ли указанные точки в наборе A
print('Point(4, 6) in A:', Point(4, 6) in A, '| Point(9, 9) in A:', Point(9, 9) in A)

# Проверяем сложение и вычитание точек, а также длину вектора от начала координат
print('p1 + p2 =', A[0] + A[1], '| p1 - p2 =', A[0] - A[1], '| |p2| =', round(abs(A[1]), 3))

# Вычисляем расстояние между двумя точками
print('расстояние A[0]–A[1]:', A[0].distance_to(A[1]))

# Объединяем наборы A и B
C = A + B
print('A + B =', C, '| len =', len(C))

# Находим центр масс объединённого набора
print('центр масс C:', C.centroid())

# Находим точку, ближайшую к координатам (6, 0)
print('ближайшая к (6; 0):', C.nearest_to(Point(6, 0)))

# Находим нижний левый и верхний правый углы ограничивающего прямоугольника
lo, hi = C.bounding_box()
print('ограничивающий прямоугольник:', lo, '–', hi)

# Заменяем первую точку набора C
C[0] = Point(10, 10)
print('после замены C[0]:', C)

# Перебираем и выводим точки набора B с порядковыми номерами
for number, point in enumerate(B, 1):
    print(f'B{number}: {point}')