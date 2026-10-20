# Лабораторная работа 1, задание 4. Класс «Фильм»
class Movie:
    # конструктор: вызывается автоматически при создании объекта
    def __init__(self, name, filmmaker, release, style, score, length_min):
        # атрибуты экземпляра: у каждого фильма свои значения
        self.name = name                   # название
        self.filmmaker = filmmaker         # режиссёр
        self.release = release             # год выхода
        self.style = style                 # жанр
        self.score = score                 # рейтинг 0.0–10.0
        self.length_min = length_min       # длительность, мин

    # классикой считается фильм, вышедший до 2000 года
    def is_classic(self):
        return self.release < 2000

    # собираем описание из атрибутов конкретного объекта (self)
    def describe(self):
        return (f'«{self.name}» ({self.release}), реж. {self.filmmaker}, '
                f'жанр: {self.style}, рейтинг {self.score}')

    def duration_hours(self):
        # divmod возвращает целую часть (часы) и остаток (минуты)
        hrs, mins = divmod(self.length_min, 60)
        return f'{hrs} ч {mins} мин'


# создаём три объекта одного класса с разными данными
library = [
    Movie('Начало', 'Кристофер Нолан', 2010, 'фантастика', 8.8, 148),
    Movie('Интерстеллар', 'Кристофер Нолан', 2014, 'фантастика', 8.7, 169),
    Movie('Матрица', 'Лана Вачовски', 1999, 'боевик', 8.7, 136),
]

# вызываем методы у каждого объекта в цикле
for film in library:
    print(film.describe())
    print(f'классика: {film.is_classic()}, длительность: {film.duration_hours()}')

# max с lambda-ключом выбирает фильм с наибольшим рейтингом
top = max(library, key=lambda f: f.score)
print('Лучший по рейтингу:', top.name)