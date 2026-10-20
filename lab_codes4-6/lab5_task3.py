# Лабораторная работа 5, задание 3. Многочлен (Polynomial)
import math


# Класс для работы с многочленами
class Polynomial:
    def __init__(self, coefs):
        self.coefs = list(coefs)  # Индекс элемента = степень x
        # Удаляем нулевые коэффициенты старших степеней
        while len(self.coefs) > 1 and self.coefs[-1] == 0:
            self.coefs.pop()

    # Сложение двух многочленов
    def __add__(self, o):
        n = max(len(self), len(o))
        return Polynomial([(self.coefs + [0] * n)[i] + (o.coefs + [0] * n)[i] for i in range(n)])

    # Меняем знак всех коэффициентов
    def __neg__(self):
        return Polynomial([-c for c in self.coefs])

    # Вычитание многочленов через сложение с противоположным
    def __sub__(self, o):
        return self + (-o)

    # Умножение многочленов
    def __mul__(self, o):
        res = [0] * (len(self) + len(o) - 1)
        # Перемножаем коэффициенты и складываем результаты одинаковых степеней
        for i, x in enumerate(self.coefs):
            for j, y in enumerate(o.coefs):
                res[i + j] += x * y
        return Polynomial(res)

    # Количество коэффициентов
    def __len__(self):
        return len(self.coefs)

    # Получение коэффициента по индексу
    def __getitem__(self, i):
        return self.coefs[i]

    # Изменение коэффициента по индексу
    def __setitem__(self, i, v):
        self.coefs[i] = v

    # Вычисление значения многочлена при заданном x
    def __call__(self, x):
        return sum(c * x ** i for i, c in enumerate(self.coefs))

    # Проверка равенства двух многочленов
    def __eq__(self, o):
        return self.coefs == o.coefs

    # Представление объекта для отладки
    def __repr__(self):
        return f'Polynomial({self.coefs})'

    # Преобразование многочлена в привычную математическую запись
    def __str__(self):
        parts = []
        for i in range(len(self) - 1, -1, -1):
            c = self.coefs[i]
            # Пропускаем нулевые коэффициенты, если многочлен не константа
            if c == 0 and len(self) > 1:
                continue
            body = (f'{abs(c)}' if (abs(c) != 1 or i == 0) else '') + ('x' if i else '') + (f'^{i}' if i > 1 else '')
            parts.append(('-' if c < 0 else '+') + ' ' + body)
        text = ' '.join(parts)
        return text[2:] if text.startswith('+') else '-' + text[2:]

    # Степень многочлена
    def degree(self):
        return len(self) - 1

    # Находим производную многочлена
    def derivative(self):
        return Polynomial([i * c for i, c in enumerate(self.coefs)][1:] or [0])


# Создаём два многочлена
f = Polynomial([-4, 3, 2])  # 2x^2 + 3x - 4
g = Polynomial([1, -1])  # -x + 1

# Выводим многочлены и представление объекта
print('f =', f, '| g =', g, '| repr:', repr(g))

# Проверяем сложение, вычитание и умножение
print('f + g =', f + g, '| f - g =', f - g, '| f * g =', f * g)

# Проверяем степень, количество коэффициентов и получение коэффициента
print('степень f:', f.degree(), '| len(f):', len(f), '| f[1] =', f[1])

# Вычисляем значение f(2) и производную f
print('f(2) =', f(2), '| f\'(x) =', f.derivative())

# Меняем свободный коэффициент и проверяем равенство многочленов
f[0] = -5
print('после f[0] = -5:', f, '| f == g:', f == g)

# Проверяем теорему Виета для уравнения 2x^2 - 14x + 24 = 0
eq = Polynomial([24, -14, 2])

# Вычисляем дискриминант квадратного уравнения
d = eq[1] ** 2 - 4 * eq[2] * eq[0]

# Находим два корня уравнения по формуле
r1, r2 = (-eq[1] + math.sqrt(d)) / (2 * eq[2]), (-eq[1] - math.sqrt(d)) / (2 * eq[2])
print(f'Уравнение {eq} = 0, корни: {r1:.0f} и {r2:.0f}')

# Проверяем теорему Виета: сумма корней = -b/a, произведение = c/a
print(f'сумма {r1 + r2:.0f} = -b/a = {-eq[1] / eq[2]:.0f}; произведение {r1 * r2:.0f} = c/a = {eq[0] / eq[2]:.0f}')

# Проверяем, что оба найденных корня обращают многочлен в ноль
print('p(r1) =', eq(r1), ', p(r2) =', eq(r2))