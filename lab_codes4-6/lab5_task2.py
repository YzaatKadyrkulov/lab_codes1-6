# Лабораторная работа 5, задание 2. Вектор в 3D (Vector3D)
import math


# Класс для работы с трёхмерными векторами
class Vector3D:
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c  # Координаты вектора x, y, z

    # Сложение двух векторов
    def __add__(self, o): return Vector3D(self.a + o.a, self.b + o.b, self.c + o.c)

    # Вычитание двух векторов
    def __sub__(self, o): return Vector3D(self.a - o.a, self.b - o.b, self.c - o.c)

    # Умножение вектора на число
    def __mul__(self, k): return Vector3D(self.a * k, self.b * k, self.c * k)

    # Изменение направления вектора на противоположное
    def __neg__(self): return Vector3D(-self.a, -self.b, -self.c)

    # Возвращаем длину вектора при использовании abs()
    def __abs__(self): return self.length()

    # Проверяем равенство координат двух векторов
    def __eq__(self, o): return (self.a, self.b, self.c) == (o.a, o.b, o.c)

    # Количество координат трёхмерного вектора
    def __len__(self): return 3

    # Строковое представление вектора для print()
    def __str__(self): return f'({self.a}, {self.b}, {self.c})'

    # Представление объекта для отладки
    def __repr__(self): return f'Vector3D({self.a}, {self.b}, {self.c})'

    # Вычисляем длину вектора по теореме Пифагора
    def length(self): return math.sqrt(self.a ** 2 + self.b ** 2 + self.c ** 2)

    # Скалярное произведение двух векторов
    def dot(self, o): return self.a * o.a + self.b * o.b + self.c * o.c

    # Векторное произведение двух векторов
    def cross(self, o):
        return Vector3D(self.b * o.c - self.c * o.b,
                        self.c * o.a - self.a * o.c,
                        self.a * o.b - self.b * o.a)

    # Нормализация: создаём вектор длины 1 с тем же направлением
    def normalize(self):
        n = self.length()
        return Vector3D(round(self.a / n, 3), round(self.b / n, 3), round(self.c / n, 3))

    # Вычисляем угол между векторами в градусах
    def angle_between(self, o):
        cos = self.dot(o) / (self.length() * o.length())
        return round(math.degrees(math.acos(cos)), 2)


# Создаём два вектора для проверки операций
u, w = Vector3D(2, -1, 3), Vector3D(4, 5, -1)
print('u =', u, '| w =', w, '| repr:', repr(u))

# Проверяем сложение, вычитание, умножение на число и смену знака
print('u + w =', u + w, '| u - w =', u - w, '| u * 3 =', u * 3, '| -u =', -u)

# Выводим длину вектора и количество его координат
print('|u| =', round(abs(u), 3), '| len(u) =', len(u))

# Вычисляем скалярное и векторное произведения
print('u · w =', u.dot(w), '| u × w =', u.cross(w))

# Получаем нормализованный вектор и угол между векторами
print('normalize(w) =', w.normalize())
print('угол между u и w =', u.angle_between(w), '°')

# Проверяем перпендикулярность: скалярное произведение равно нулю
e1, e2 = Vector3D(0, 3, 0), Vector3D(5, 0, 0)
print('ортогональны ли (0,3,0) и (5,0,0):', e1.dot(e2) == 0, '| угол', e1.angle_between(e2), '°')

# Проверяем равенство двух векторов
print('u == Vector3D(2, -1, 3):', u == Vector3D(2, -1, 3))