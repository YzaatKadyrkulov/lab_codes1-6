# Лабораторная работа 4, задание 3. Напитки в кафе
from abc import ABC, abstractmethod


# Абстрактный базовый класс для всех напитков
class Beverage(ABC):
    # Каждый напиток должен иметь описание, калорийность и цену
    @abstractmethod
    def description(self): ...

    @abstractmethod
    def calories(self): ...

    @abstractmethod
    def price(self): ...

    # Общий метод для вывода информации о напитке
    def line(self):
        return f'{self.description():<34} {self.calories():>4} ккал  {self.price():>4} сом'


# Класс кофе
class Coffee(Beverage):
    def __init__(self, sort, ml, with_milk, sugar_spoons):
        self.sort, self.ml, self.with_milk, self.sugar_spoons = sort, ml, with_milk, sugar_spoons

    # Формируем описание кофе с учётом молока
    def description(self):
        return f'Кофе {self.sort} {self.ml} мл' + (' с молоком' if self.with_milk else '')

    # Рассчитываем калории с учётом молока и сахара
    def calories(self):
        return 5 + (60 if self.with_milk else 0) + self.sugar_spoons * 20

    # Рассчитываем стоимость кофе
    def price(self):
        return 90 + self.ml // 10 + (20 if self.with_milk else 0)


# Класс чая
class Tea(Beverage):
    def __init__(self, sort, ml, extras):
        self.sort, self.ml, self.extras = sort, ml, extras

    # Добавляем к описанию чая дополнительные ингредиенты
    def description(self):
        return f'Чай {self.sort} {self.ml} мл' + (f' ({", ".join(self.extras)})' if self.extras else '')

    # Каждый дополнительный ингредиент добавляет 25 калорий
    def calories(self):
        return 2 + len(self.extras) * 25

    # Рассчитываем цену с учётом количества добавок
    def price(self):
        return 60 + len(self.extras) * 15


# Класс сока
class Juice(Beverage):
    def __init__(self, fruit, ml, natural, concentration):
        self.fruit, self.ml, self.natural, self.concentration = fruit, ml, natural, concentration

    # Указываем фрукт, объём и тип сока
    def description(self):
        return f'Сок {self.fruit} {self.ml} мл ({"натуральный" if self.natural else "нектар"})'

    # Рассчитываем калорийность с учётом объёма и концентрации
    def calories(self):
        return round(self.ml * 0.45 * self.concentration / 100)

    # Натуральный сок стоит дороже нектара
    def price(self):
        return 110 if self.natural else 70


# Класс смузи
class Smoothie(Beverage):
    def __init__(self, parts, ml, base):
        self.parts, self.ml, self.base = parts, ml, base

    # Формируем описание смузи и перечисляем его ингредиенты
    def description(self):
        return f'Смузи {self.base} {self.ml} мл: ' + ', '.join(self.parts)

    # Рассчитываем калорийность в зависимости от объёма
    def calories(self):
        return round(self.ml * 0.55)

    # Цена зависит от количества ингредиентов
    def price(self):
        return 130 + 10 * len(self.parts)


# Создаём меню из разных напитков
menu = [
    Coffee('латте', 300, True, 1),
    Coffee('эспрессо', 60, False, 0),
    Tea('зелёный', 400, ['мята', 'лимон']),
    Juice('яблочный', 250, True, 100),
    Smoothie(['шпинат', 'банан'], 350, 'овощной'),
]

# Выводим описание, калорийность и цену каждого напитка
for drink in menu:
    print(drink.line())

# Находим напиток с наименьшей калорийностью
light = min(menu, key=lambda d: d.calories())
print('Самый низкокалорийный:', light.description(), f'({light.calories()} ккал)')