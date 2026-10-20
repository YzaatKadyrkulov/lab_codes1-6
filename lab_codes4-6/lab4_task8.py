# Лабораторная работа 4, задание 8. Транспортные маршруты
from abc import ABC, abstractmethod


# Абстрактный базовый класс для всех видов поездок
class Trip(ABC):
    # Каждый вид транспорта должен рассчитывать цену, время и выбросы CO₂
    @abstractmethod
    def cost(self): ...

    @abstractmethod
    def duration_hours(self): ...

    @abstractmethod
    def co2_emission(self): ...  # Выбросы CO₂ в кг на пассажира

    # Возвращаем название класса как название транспорта
    def title(self):
        return type(self).__name__


# Класс поездки на такси
class TaxiTrip(Trip):
    def __init__(self, km, per_km, tariff, rush):
        self.km, self.per_km, self.tariff, self.rush = km, per_km, tariff, rush

    # Рассчитываем стоимость с учётом тарифа и пробок
    def cost(self):
        k = {'эконом': 1.0, 'комфорт': 1.4, 'бизнес': 2.0}[self.tariff]
        return round(self.km * self.per_km * k * (1.3 if self.rush else 1))

    # Рассчитываем время поездки с учётом пробок
    def duration_hours(self):
        return self.km / (30 if self.rush else 60)

    # Рассчитываем выбросы CO₂ на километр
    def co2_emission(self):
        return self.km * 0.17


# Класс поездки на автобусе
class BusTrip(Trip):
    def __init__(self, route, ticket, changes, km):
        self.route, self.ticket, self.changes, self.km = route, ticket, changes, km

    # Цена поездки равна стоимости билета
    def cost(self):
        return self.ticket

    # Время зависит от расстояния и количества пересадок
    def duration_hours(self):
        return self.km / 50 + self.changes * 0.7

    # Рассчитываем выбросы CO₂ на пассажира
    def co2_emission(self):
        return self.km * 0.05


# Класс авиаперелёта
class AirTrip(Trip):
    def __init__(self, km, klass, luggage_kg):
        self.km, self.klass, self.luggage_kg = km, klass, luggage_kg

    # Рассчитываем цену в зависимости от класса и веса багажа
    def cost(self):
        k = {'эконом': 1.0, 'бизнес': 2.8, 'первый': 4.5}[self.klass]
        return round(self.km * 0.9 * k + self.luggage_kg * 40)

    # К времени полёта добавляем 2,5 часа на аэропорт
    def duration_hours(self):
        return self.km / 800 + 2.5

    # Рассчитываем выбросы CO₂ на пассажира
    def co2_emission(self):
        return self.km * 0.15


# Класс поездки на поезде
class TrainTrip(Trip):
    def __init__(self, km, wagon, speed):
        self.km, self.wagon, self.speed = km, wagon, speed

    # Цена зависит от расстояния и типа вагона
    def cost(self):
        k = {'плацкарт': 1.0, 'купе': 1.6, 'СВ': 2.6}[self.wagon]
        return round(self.km * 1.1 * k)

    # Рассчитываем время по расстоянию и скорости поезда
    def duration_hours(self):
        return self.km / self.speed

    # Рассчитываем выбросы CO₂ на пассажира
    def co2_emission(self):
        return self.km * 0.03


# Создаём список вариантов поездки
options = [
    TaxiTrip(240, 25, 'комфорт', False),
    BusTrip('Бишкек – Ош', 1400, 1, 660),
    AirTrip(660, 'эконом', 0),
    TrainTrip(660, 'купе', 55),
]

# Выводим таблицу со стоимостью, временем и выбросами
print(f'{"Вид":<10}{"Цена, сом":>10}{"Время, ч":>10}{"CO₂, кг":>9}')
for t in options:
    print(f'{t.title():<10}{t.cost():>10}{t.duration_hours():>10.1f}{t.co2_emission():>9.1f}')

# Находим самый дешёвый, быстрый и экологичный варианты
cheap = min(options, key=lambda t: t.cost())
fast = min(options, key=lambda t: t.duration_hours())
green = min(options, key=lambda t: t.co2_emission())

print('Дешевле всех:', cheap.title(), '| Быстрее всех:', fast.title(), '| Экологичнее:', green.title())

# Оцениваем каждый вариант по трём критериям:
# стоимость, время поездки и выбросы CO₂
score = lambda t: (
    t.cost() / cheap.cost()
    + t.duration_hours() / fast.duration_hours()
    + t.co2_emission() / green.co2_emission()
)

# Выбираем вариант с наименьшей общей оценкой
print('Оптимальный (по сумме трёх критериев):', min(options, key=score).title())