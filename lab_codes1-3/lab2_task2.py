# Лабораторная работа 2, задание 2. Класс «Студенческий билет»
class StudentCard:
    def __init__(self, fio, number, score):
        # приватные атрибуты (name mangling): снаружи класса напрямую недоступны
        self.__name = fio
        self.__card_id = number
        # присваивание идёт через сеттер, поэтому проверка работает
        # уже при создании объекта
        self.gpa = score

    # геттер: вызывается при чтении card.gpa
    @property
    def gpa(self):
        return self.__gpa

    # сеттер: вызывается при записи card.gpa = x, проверяет значение перед сохранением
    @gpa.setter
    def gpa(self, value):
        if not 0.0 <= value <= 4.0:
            # недопустимое значение — выбрасываем исключение
            raise ValueError(f'GPA {value} вне диапазона 0.0–4.0')
        self.__gpa = value

    # вычисляемое свойство: не хранится в объекте, а определяется по текущему GPA
    @property
    def status(self):
        if self.__gpa >= 3.5:
            return 'Отличник'
        if self.__gpa >= 2.5:
            return 'Хорошист'
        if self.__gpa >= 1.0:
            return 'Удовлетворительно'
        return 'Отчислен'

    # строка для print(): :<20 выравнивает ФИО по левому краю в 20 символов
    def __str__(self):
        return f'{self.__card_id} | {self.__name:<20} | GPA {self.__gpa} | {self.status}'


# создаём пять студенческих билетов с разным GPA
cards = [
    StudentCard('Орозалиев Акылбек', 'СБ-1001', 3.9),
    StudentCard('Совхозова Сабина', 'СБ-1002', 3.1),
    StudentCard('Толкунов Адилет', 'СБ-1003', 2.0),
    StudentCard('Сапарбекова Адинай', 'СБ-1004', 3.6),
    StudentCard('Жашарбеков Эмиржан', 'СБ-1005', 0.7),
]
for c in cards:
    print(c)

# статистика: средний GPA и число отличников
avg = sum(c.gpa for c in cards) / len(cards)
top_count = sum(1 for c in cards if c.status == 'Отличник')
print(f'Средний GPA: {avg:.2f}; отличников: {top_count}')

# проверяем валидацию: значение вне диапазона вызывает ValueError
try:
    cards[0].gpa = 4.8
except ValueError as err:
    print('Ошибка валидации:', err)