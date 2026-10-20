# Лабораторная работа 2, задание 3. Класс «Медицинская карта»
class MedCard:
    def __init__(self, person, years, blood):
        # приватные атрибуты (name mangling): снаружи класса напрямую недоступны
        self.__patient = person
        # присваивание идёт через сеттер, поэтому проверка работает
        # уже при создании объекта
        self.age = years
        self.__blood = blood
        self.__illnesses = []              # список диагнозов, скрыт от внешнего кода

    # геттер: вызывается при чтении card.age
    @property
    def age(self):
        return self.__age

    # сеттер: возраст допустим только в диапазоне 0–150
    @age.setter
    def age(self, value):
        if not 0 <= value <= 150:
            # недопустимое значение — выбрасываем исключение
            raise ValueError('Возраст должен быть в диапазоне 0–150')
        self.__age = value

    # вычисляемое свойство: не хранится в объекте, определяется по возрасту
    @property
    def is_adult(self):
        return self.__age >= 18

    # не добавляем один и тот же диагноз дважды
    def add_diagnosis(self, text):
        if text not in self.__illnesses:
            self.__illnesses.append(text)

    # удаляем диагноз только если он есть в списке (иначе remove вызвал бы ошибку)
    def remove_diagnosis(self, text):
        if text in self.__illnesses:
            self.__illnesses.remove(text)

    # полная сводка по карте одной строкой
    def summary(self):
        # если диагнозов нет, join вернёт пустую строку, тогда подставится «нет записей»
        ill = ', '.join(self.__illnesses) or 'нет записей'
        adult = 'взрослый' if self.is_adult else 'ребёнок'
        return (f'{self.__patient} ({adult}, {self.__age} лет), '
                f'группа крови {self.__blood}; диагнозы: {ill}')


# создаём три карты и заполняем их диагнозами
c1 = MedCard('Абасбеков Калыкожо', 45, 'A(II)+')
c1.add_diagnosis('гипертония')
c1.add_diagnosis('гастрит')
c2 = MedCard('Саякбаева Айзат', 9, '0(I)+')
c2.add_diagnosis('аллергический ринит')
c3 = MedCard('Нусупов Темирлан', 67, 'B(III)-')
c3.add_diagnosis('диабет 2 типа')
c3.add_diagnosis('артрит')
c3.remove_diagnosis('артрит')              # удаляем диагноз
for card in (c1, c2, c3):
    print(card.summary())

# проверяем валидацию: возраст вне диапазона вызывает ValueError
try:
    c2.age = 200
except ValueError as err:
    print('Ошибка:', err)