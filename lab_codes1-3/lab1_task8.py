# Лабораторная работа 1, задание 8. Класс «Метеостанция»
class WeatherStation:
    # конструктор: вызывается автоматически при создании объекта
    def __init__(self, label, town, height, temp, wet, wind):
        # атрибуты экземпляра: у каждой станции свои значения
        self.label = label                 # название станции
        self.town = town                   # город
        self.height = height               # высота над уровнем моря, м
        self.temp = temp                   # температура, °C
        self.wet = wet                     # влажность, %
        self.wind = wind                   # скорость ветра, м/с

    # собираем описание из атрибутов конкретного объекта (self)
    def describe(self):
        return (f'Станция «{self.label}» ({self.town}, {self.height} м): '
                f'{self.temp}°C, влажность {self.wet}%, ветер {self.wind} м/с')

    # ветер понижает ощущаемую температуру; round() округляет результат
    def feels_like(self):
        return round(self.temp - self.wind * 0.7)

    # статус погоды определяется по порогам температуры (от высшего к низшему)
    def weather_status(self):
        if self.temp > 30:
            return 'Жарко'
        if self.temp > 15:
            return 'Тепло'
        if self.temp > 5:
            return 'Прохладно'
        return 'Холодно'

    # цепочечное сравнение: должны выполняться оба условия сразу
    def is_comfortable(self):
        return 40 <= self.wet <= 70 and 18 <= self.temp <= 26


# создаём три объекта одного класса с разными данными
net = [
    WeatherStation('Ала-Тоо', 'Бишкек', 800, 28.0, 45, 2.5),
    WeatherStation('Иссык-Куль', 'Чолпон-Ата', 1650, 22.0, 55, 3.0),
    WeatherStation('Памир', 'Мургаб', 3650, 3.0, 30, 9.0),
]

# вызываем методы у каждой станции в цикле
for st in net:
    print(st.describe())
    print(f'ощущается как {st.feels_like()}°C, {st.weather_status()}, '
          f'комфортно: {st.is_comfortable()}')