# Лабораторная работа 1, задание 5. Класс «Планета»
class Planet:
    # атрибут класса: общий для всех планет
    body_type = 'Небесное тело'

    # конструктор: вызывается автоматически при создании объекта
    def __init__(self, title, diam, mass_ratio, satellites, air):
        # атрибуты экземпляра: у каждой планеты свои значения
        self.title = title
        self.diam = diam                   # диаметр, км
        self.mass_ratio = mass_ratio       # масса относительно Земли
        self.satellites = satellites
        self.air = air                     # есть ли атмосфера

    # собираем описание из атрибутов конкретного объекта (self)
    def describe(self):
        # условное выражение: булево значение превращаем в слово
        atm = 'есть' if self.air else 'нет'
        return (f'{self.title}: диаметр {self.diam} км, масса {self.mass_ratio} M⊕, '
                f'спутников {self.satellites}, атмосфера: {atm}')

    # ускорение свободного падения пропорционально массе планеты;
    # earth_g — параметр со значением по умолчанию
    def gravity(self, earth_g=9.8):
        return round(earth_g * self.mass_ratio, 2)

    # гигантом считается планета с диаметром больше 50 000 км
    def is_giant(self):
        return self.diam > 50000


# создаём три объекта одного класса с разными данными
cosmos = [
    Planet('Земля', 12742, 1.0, 1, True),
    Planet('Марс', 6779, 0.107, 2, True),
    Planet('Юпитер', 139820, 317.8, 95, True),
]

# к атрибуту класса обращаемся через имя класса
print(Planet.body_type)

# вызываем методы у каждого объекта в цикле
for body in cosmos:
    print(body.describe())
    print(f'гравитация: {body.gravity()} м/с², гигант: {body.is_giant()}')

# max с lambda-ключом выбирает планету с наибольшим диаметром
biggest = max(cosmos, key=lambda p: p.diam)
print('Самая большая планета:', biggest.title)