# Лабораторная работа 3, задание 4. Спортсмены
# родительский класс: общие данные и поведение всех спортсменов
class Athlete:
    def __init__(self, fio, years, country):
        self.fio = fio
        self.years = years
        self.country = country
        self.prizes = []                     # список наград: пары (медаль, год)

    # награда хранится как пара (медаль, год)
    def add_medal(self, medal, year):
        self.prizes.append((medal, year))

    def medals_count(self):
        return len(self.prizes)

    def achievement(self):
        # считаем золотые медали: «_» означает, что год нам здесь не нужен
        gold = sum(1 for m, _ in self.prizes if m == 'золото')
        return f'{self.fio} ({self.country}): наград {self.medals_count()}, золотых {gold}'

    # в базовом классе скорость неизвестна: потомки переопределяют метод
    def avg_speed(self):
        return 0.0


# наследование: пловец получает все методы Athlete и дополняет их
class Swimmer(Athlete):
    def __init__(self, fio, years, country, style, record_100):
        # вызываем конструктор родителя для общих атрибутов
        super().__init__(fio, years, country)
        # атрибуты, которые есть только у пловца
        self.style = style
        self.record_100 = record_100         # секунды на 100 м

    # переопределение: скорость = 100 м / время рекорда
    def avg_speed(self):
        return round(100 / self.record_100, 2)

    # расширяем метод родителя через super(), а не копируем его
    def achievement(self):
        return f'{super().achievement()}; стиль: {self.style}, рекорд 100 м: {self.record_100} с'


class Sprinter(Athlete):
    def __init__(self, fio, years, country, dist, record, starts):
        super().__init__(fio, years, country)
        # дистанция, личный рекорд на ней (с) и число стартов
        self.dist, self.record, self.starts = dist, record, starts

    # переопределение: скорость = дистанция / время рекорда
    def avg_speed(self):
        return round(self.dist / self.record, 2)

    def achievement(self):
        return f'{super().achievement()}; дистанция {self.dist} м, стартов: {self.starts}'


# команда: два пловца и два спринтера в одном списке
team = [
    Swimmer('Каныбек Асанов', 22, 'Кыргызстан', 'вольный', 49.8),
    Swimmer('Лена Миллер', 25, 'Германия', 'баттерфляй', 56.4),
    Sprinter('Усейн Мурзалиев', 24, 'Кыргызстан', 100, 10.4, 35),
    Sprinter('Томас Грин', 27, 'Канада', 200, 20.6, 41),
]

# добавляем награды спортсменам
team[0].add_medal('золото', 2024)
team[0].add_medal('серебро', 2025)
team[1].add_medal('бронза', 2023)
team[2].add_medal('золото', 2025)
team[2].add_medal('золото', 2026)
team[3].add_medal('серебро', 2024)

# полиморфный цикл: вызовы одинаковые, а выполняется версия метода
# в соответствии с типом объекта
for sp in team:
    print(sp.achievement())
    print(f'средняя скорость: {sp.avg_speed()} м/с')

# самый быстрый — по средней скорости (max с lambda-ключом)
best = max(team, key=lambda a: a.avg_speed())
print('Самый быстрый:', best.fio, '-', best.avg_speed(), 'м/с')