# Лабораторная работа 3, задание 8. Горные вершины
# родительский класс: общие данные и методы для любой горы
class Mountain:
    def __init__(self, name, metres, land, first_up):
        self.name = name
        self.metres = metres               # высота, м
        self.land = land                   # страна
        self.first_up = first_up           # год первого восхождения

    def describe(self):
        return f'{self.name} ({self.land}), {self.metres} м, первое восхождение {self.first_up}'

    # высокогорье — выше 5000 м; метод наследуется потомками без изменений
    def is_highaltitude(self):
        return self.metres > 5000

    # в базовом классе сложность не определена: потомки переопределяют метод
    def climbing_difficulty(self):
        return 'не определена'


# наследование: вершина получает все методы Mountain и дополняет их
class Peak(Mountain):
    # словесные оценки категорий сложности 1–5
    LEVELS = {1: 'простая', 2: 'умеренная', 3: 'серьёзная', 4: 'очень сложная', 5: 'экстремальная'}

    def __init__(self, name, metres, land, first_up, grade, route, length_km):
        # вызываем конструктор родителя для общих атрибутов
        super().__init__(name, metres, land, first_up)
        # атрибуты, которые есть только у вершины: категория, тип маршрута, длина
        self.grade, self.route, self.length_km = grade, route, length_km

    # расширяем описание родителя через super(), а не копируем его
    def describe(self):
        return f'{super().describe()}; маршрут {self.route}, {self.length_km} км'

    # переопределение: сложность определяется по категории вершины
    def climbing_difficulty(self):
        return f'{self.LEVELS[self.grade]} (категория {self.grade}/5)'


class Volcano(Mountain):
    def __init__(self, name, metres, land, first_up, state, last_eruption, crater_m):
        super().__init__(name, metres, land, first_up)
        # статус, год последнего извержения, диаметр кратера
        self.state, self.last_eruption, self.crater_m = state, last_eruption, crater_m

    def describe(self):
        return f'{super().describe()}; {self.state}, кратер {self.crater_m} м'

    # переопределение: сложность вулкана зависит от его статуса
    def climbing_difficulty(self):
        return {'активный': 'опасно, нужен допуск', 'спящий': 'средняя',
                'потухший': 'низкая'}[self.state]


# вершины и вулканы в одном списке
peaks = [git remote add origin https://github.com/YzaatKadyrkulov/lab_codes1-6.git
    Peak('Пик Победы', 7439, 'Кыргызстан', 1938, 5, 'ледовый', 18),
    Peak('Пик Ленина', 7134, 'Кыргызстан/Таджикистан', 1928, 3, 'смешанный', 14),
    Peak('Пик Корона', 4860, 'Кыргызстан', 1954, 2, 'скальный', 8),
    Volcano('Эльбрус', 5642, 'Россия', 1829, 'спящий', 50, 250),
    Volcano('Сент-Хеленс', 2549, 'США', 1853, 'активный', 2008, 1700),
    Volcano('Фудзи', 3776, 'Япония', 663, 'спящий', 1707, 600),
]

# одинаковые вызовы для объектов разных классов (полиморфизм):
# describe() и climbing_difficulty() работают по правилам конкретного класса
for m in peaks:
    print(m.describe())
    print(f'высокогорье: {m.is_highaltitude()}, сложность: {m.climbing_difficulty()}')