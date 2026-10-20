# Лабораторная работа 3, задание 2. Туристическое агентство
# родительский класс: общие данные и поведение всех туров
class TourPackage:
    def __init__(self, tour_name, land, nights, cost):
        self.tour_name = tour_name
        self.land = land
        self.nights = nights               # продолжительность, дней
        self.cost = cost                   # базовая цена на человека, $

    def season_discount(self, month):
        return 0                           # в базовом классе скидок нет

    def total_price(self, persons):
        return self.cost * persons * (1 - self.season_discount(1) / 100)

    def describe(self):
        return f'{self.tour_name} ({self.land}, {self.nights} дн., от ${self.cost})'


# потомок: добавляет атрибуты пляжного отдыха
class BeachTour(TourPackage):
    # доплата за питание на человека, $ (BB — завтраки, HB — полупансион, AI — всё включено)
    MEALS = {'BB': 0, 'HB': 120, 'AI': 300}

    def __init__(self, tour_name, land, nights, cost, resort, stars, flight, meals):
        # вызываем конструктор родителя для общих атрибутов
        super().__init__(tour_name, land, nights, cost)
        # атрибуты, которые есть только у пляжного тура
        self.resort, self.stars, self.flight, self.meals = resort, stars, flight, meals

    # переопределение: бархатный сезон (май, сентябрь, октябрь), скидка 15%
    def season_discount(self, month):
        return 15 if month in (9, 10, 5) else 0

    # переопределение: цена с учётом питания, перелёта и сезонной скидки
    def total_price(self, persons, month=7):
        extra = self.MEALS[self.meals] + (250 if self.flight else 0)
        base = (self.cost + extra) * persons
        return round(base * (1 - self.season_discount(month) / 100))

    # расширяем описание родителя через super(), а не копируем его
    def describe(self):
        fly = 'с перелётом' if self.flight else 'без перелёта'
        return f'{super().describe()} | {self.resort}, {self.stars}*, {self.meals}, {fly}'


# потомок: добавляет атрибуты приключенческого тура
class AdventureTour(TourPackage):
    def __init__(self, tour_name, land, nights, cost, route, fitness, gear, guide):
        super().__init__(tour_name, land, nights, cost)
        self.route, self.fitness, self.gear, self.guide = route, fitness, gear, guide

    # переопределение: зимой (ноябрь–март) скидка 20%
    def season_discount(self, month):
        return 20 if month in (11, 12, 1, 2, 3) else 0

    # переопределение: если гид включён, добавляем его стоимость ($80 на человека)
    def total_price(self, persons, month=7):
        base = (self.cost + (80 if self.guide else 0)) * persons
        return round(base * (1 - self.season_discount(month) / 100))

    def describe(self):
        return f'{super().describe()} | {self.route}, подготовка: {self.fitness}'


# по три тура каждого вида в одном списке
tours = [
    BeachTour('Лето на Иссык-Куле', 'Кыргызстан', 7, 400, 'Чолпон-Ата', 4, False, 'HB'),
    BeachTour('Анталья', 'Турция', 10, 700, 'Кемер', 5, True, 'AI'),
    BeachTour('Дубай', 'ОАЭ', 6, 900, 'Джумейра', 5, True, 'BB'),
    AdventureTour('Каракол–Алтын-Арашан', 'Кыргызстан', 5, 350, 'пеший маршрут', 'средний',
                  ['палатка', 'треккинг-палки'], True),
    AdventureTour('Сон-Куль верхом', 'Кыргызстан', 4, 300, 'конный поход', 'лёгкий', ['седло'], True),
    AdventureTour('Ала-Арча: ледник', 'Кыргызстан', 3, 250, 'ледовый', 'сложный', ['кошки', 'ледоруб'], False),
]

# один цикл работает и с пляжными, и с приключенческими турами (полиморфизм):
# вызовы одинаковые, а считается по правилам конкретного класса
for t in tours:
    print(t.describe())
    print(f'на 2 человек в июле: ${t.total_price(2, 7)}, в октябре: ${t.total_price(2, 10)}, '
          f'в январе: ${t.total_price(2, 1)}')