# Лабораторная работа 4, задание 5. Страховые продукты
from abc import ABC, abstractmethod


# Абстрактный базовый класс для всех страховых продуктов
class Insurance(ABC):
    # Каждый вид страховки должен рассчитывать месячную стоимость и описание
    @abstractmethod
    def monthly_premium(self): ...

    @abstractmethod
    def description(self): ...

    # Общий метод: рассчитываем стоимость страховки за год
    def annual_premium(self):
        return round(self.monthly_premium() * 12, 2)


# Класс страхования автомобиля
class CarInsurance(Insurance):
    def __init__(self, car_cost, driver_exp, vehicle, crashes):
        self.car_cost, self.driver_exp, self.vehicle, self.crashes = car_cost, driver_exp, vehicle, crashes

    # Рассчитываем месячную страховку с учётом стоимости машины,
    # опыта водителя и количества аварий
    def monthly_premium(self):
        rate = 0.004 * (1 + 0.3 * self.crashes) * (0.8 if self.driver_exp > 10 else 1.0)
        return round(self.car_cost * rate, 2)

    # Возвращаем информацию об автомобильной страховке
    def description(self):
        return f'КАСКО ({self.vehicle}), аварий за 3 года: {self.crashes}'


# Класс медицинского страхования
class HealthInsurance(Insurance):
    def __init__(self, years, chronic, region, program):
        self.years, self.chronic, self.region, self.program = years, chronic, region, program

    # Стоимость зависит от программы, возраста и наличия хронических заболеваний
    def monthly_premium(self):
        base = 35 if self.program == 'базовая' else 70
        return round(base * (1 + self.years / 100) * (1.4 if self.chronic else 1), 2)

    def description(self):
        return f'Медицинская ({self.program}), регион {self.region}'


# Класс страхования путешествий
class TravelInsurance(Insurance):
    def __init__(self, days, land, kind, sport):
        self.days, self.land, self.kind, self.sport = days, land, kind, sport

    # Рассчитываем стоимость с учётом длительности поездки,
    # спортивных занятий и типа путешествия
    def monthly_premium(self):
        per_day = 2.5 * (1.5 if self.sport else 1) * (1.2 if self.kind == 'бизнес' else 1)
        return round(per_day * min(self.days, 30), 2)  # Учитываем максимум 30 дней

    def description(self):
        return f'Путешественник ({self.land}, {self.days} дн., {self.kind})'


# Класс страхования имущества
class PropertyInsurance(Insurance):
    def __init__(self, kind, cost, area, floor):
        self.kind, self.cost, self.area, self.floor = kind, cost, area, floor

    # Стоимость зависит от типа имущества, его стоимости и площади
    def monthly_premium(self):
        k = 0.0012 if self.kind == 'квартира' else 0.002
        return round(self.cost * k + self.area * 0.05, 2)

    def description(self):
        return f'Имущество: {self.kind}, {self.area} м², этаж {self.floor}'


# Создаём список страховых полисов разных типов
portfolio = [
    CarInsurance(12000, 12, 'седан', 1),
    HealthInsurance(37, True, 'Чуй', 'расширенная'),
    TravelInsurance(14, 'Турция', 'турист', True),
    PropertyInsurance('дом', 85000, 140, 1),
]

# Выводим описание и стоимость каждого полиса за месяц и год
for pol in portfolio:
    print(f'{pol.description()}')
    print(f'в месяц: ${pol.monthly_premium()}, в год: ${pol.annual_premium()}')

# Суммируем годовую стоимость всех страховых полисов
print('Годовой портфель: $', round(sum(p.annual_premium() for p in portfolio), 2))