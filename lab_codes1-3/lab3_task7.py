# Лабораторная работа 3, задание 7. Музыкальные инструменты
# родительский класс: общие данные и методы для любого инструмента
class Instrument:
    def __init__(self, title, origin, made_year, family):
        self.title = title                 # название
        self.origin = origin               # страна происхождения
        self.made_year = made_year         # год создания (примерно)
        self.family = family               # тип: струнный / духовой / ...

    def play(self):
        return f'{self.title} звучит'

    def tune(self):
        return f'{self.title} настроен'

    def describe(self):
        return f'{self.title} ({self.family}), {self.origin}, около {self.made_year} г.'


# наследование: струнный инструмент получает все методы Instrument и дополняет их
class StringInstrument(Instrument):
    def __init__(self, title, origin, made_year, strings, body, way):
        # вызываем конструктор родителя, тип семейства задаём сразу
        super().__init__(title, origin, made_year, 'струнный')
        # атрибуты, которые есть только у струнных: число струн, материал деки, способ игры
        self.strings, self.body, self.way = strings, body, way

    # переопределение: расширяем метод родителя через super(), а не копируем его
    def play(self):
        return f'{super().play()}: {self.way} способ, струн — {self.strings}'

    def tune(self):
        return f'Подтягиваем струны ({self.strings} шт., {self.body}) — {super().tune()}'


class WindInstrument(Instrument):
    def __init__(self, title, origin, made_year, notes, material, kind):
        super().__init__(title, origin, made_year, 'духовой')
        # диапазон нот, материал и тип (медный / деревянный)
        self.notes, self.material, self.kind = notes, material, kind

    def play(self):
        return f'{super().play()}: диапазон {self.notes}, {self.kind}'

    def tune(self):
        return f'Проверяем строй и мундштук ({self.material}) — {super().tune()}'


# оркестр: два струнных и два духовых инструмента в одном списке
orchestra = [
    StringInstrument('Комуз', 'Кыргызстан', 1500, 3, 'абрикос', 'щипковый'),
    StringInstrument('Скрипка', 'Италия', 1550, 4, 'ель и клён', 'смычковый'),
    WindInstrument('Сыбызгы', 'Кыргызстан', 1400, 'D–a2', 'камыш/дерево', 'деревянный'),
    WindInstrument('Труба', 'Германия', 1600, 'E–c3', 'латунь', 'медный'),
]

# полиморфизм: один и тот же вызов даёт разное поведение
# в зависимости от класса объекта
for inst in orchestra:
    print(inst.describe())
    print('   ', inst.tune())
    print('   ', inst.play())