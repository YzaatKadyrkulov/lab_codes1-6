# Лабораторная работа 5, задание 5. Время (Time)
from functools import total_ordering


# Декоратор автоматически добавляет остальные операции сравнения
@total_ordering
class Time:
    def __init__(self, hh=0, mm=0, ss=0):
        # Переводим часы, минуты и секунды в общее количество секунд
        total = hh * 3600 + mm * 60 + ss

        # Нормализуем время: получаем часы, минуты и секунды
        self.hh, rest = divmod(total, 3600)
        self.mm, self.ss = divmod(rest, 60)

    # Создаём объект времени из общего количества секунд
    @classmethod
    def from_seconds(cls, secs):
        return cls(0, 0, secs)

    # Переводим время в секунды
    def __int__(self): return self.hh * 3600 + self.mm * 60 + self.ss

    # Складываем два значения времени
    def __add__(self, o): return Time.from_seconds(int(self) + int(o))

    # Вычитаем одно время из другого
    def __sub__(self, o):
        # Проверяем, чтобы результат не был отрицательным
        if int(self) < int(o):
            raise ValueError('Результат вычитания времени отрицателен')
        return Time.from_seconds(int(self) - int(o))

    # Проверяем равенство времени
    def __eq__(self, o): return int(self) == int(o)

    # Сравниваем, какое время меньше
    def __lt__(self, o): return int(self) < int(o)

    # Проверяем, не равно ли время нулю
    def __bool__(self): return int(self) != 0

    # Выводим время в формате ЧЧ:ММ:СС
    def __str__(self): return f'{self.hh:02d}:{self.mm:02d}:{self.ss:02d}'

    # Представление объекта для отладки
    def __repr__(self): return f'Time({self.hh}, {self.mm}, {self.ss})'

    # Переводим время в минуты
    def to_minutes(self): return round(int(self) / 60, 1)


# Создаём два значения времени
t1 = Time(9, 45, 30)
t2 = Time(1, 20, 45)
print('t1 =', t1, '| t2 =', t2, '| repr:', repr(t2))

# Проверяем автоматическую нормализацию времени
print('Time(0, 75, 100) =', Time(0, 75, 100), '(нормализация)')

# Проверяем сложение и вычитание времени
print('t1 + t2 =', t1 + t2, '| t1 - t2 =', t1 - t2)

# Проверяем операции сравнения
print('t1 > t2:', t1 > t2, '| t1 <= t2:', t1 <= t2, '| t1 == Time(9, 45, 30):', t1 == Time(9, 45, 30))

# Проверяем перевод в секунды и минуты, а также создание времени из секунд
print('int(t2) =', int(t2), 'с | t2 в минутах:', t2.to_minutes(), '| from_seconds(5000) =', Time.from_seconds(5000))

# Проверяем логическое значение объекта времени
print('bool(Time()) =', bool(Time()), '| bool(t2) =', bool(t2))

# Проверяем обработку ошибки при отрицательном результате вычитания
try:
    t2 - t1
except ValueError as err:
    print('Ошибка:', err)

# Создаём расписание занятий
print('Расписание занятий:')
cursor = Time(8, 30)  # Начало первого занятия в 08:30

# Для каждого предмета вычисляем время окончания и добавляем перемену
for subject, minutes in [('Программирование', 90), ('Математика', 80), ('Английский', 60)]:
    end = cursor + Time(0, minutes)
    print(f'  {cursor}–{end}  {subject}')
    cursor = end + Time(0, 10)  # После занятия добавляем 10 минут перемены