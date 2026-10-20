# Лабораторная работа 2, задание 8. Класс «Показатели здоровья»
class HealthMetrics:
    def __init__(self, fio, cm, kg, years, sex):
        # приватные атрибуты (name mangling): снаружи класса напрямую недоступны
        self.__fio = fio
        # рост и вес присваиваются через сеттеры, поэтому проверка работает
        # уже при создании объекта
        self.height = cm
        self.weight = kg
        self.__years = years
        self.__sex = sex                     # 'м' или 'ж', нужен для формулы калорий

    # геттер: вызывается при чтении person.height
    @property
    def height(self):
        return self.__height

    # сеттер: проверка допустимого диапазона роста
    @height.setter
    def height(self, value):
        if not 50 <= value <= 250:
            raise ValueError('Рост должен быть 50–250 см')
        self.__height = value

    @property
    def weight(self):
        return self.__weight

    # сеттер: проверка допустимого диапазона веса
    @weight.setter
    def weight(self, value):
        if not 2 <= value <= 500:
            raise ValueError('Вес должен быть 2–500 кг')
        self.__weight = value

    # индекс массы тела = вес / рост² (рост переводим из сантиметров в метры)
    def bmi(self):
        return round(self.__weight / (self.__height / 100) ** 2, 1)

    # статус определяется по порогам ИМТ (от низшего к высшему)
    def bmi_status(self):
        value = self.bmi()
        if value < 18.5:
            return 'Недовес'
        if value < 25:
            return 'Норма'
        if value < 30:
            return 'Избыточный вес'
        if value < 40:
            return 'Ожирение'
        return 'Морбидное ожирение'

    def daily_calories(self):                # формула Харриса–Бенедикта
        # для краткости формул даём короткие имена: вес, рост, возраст
        w, h, a = self.__weight, self.__height, self.__years
        # коэффициенты формулы различаются для мужчин и женщин
        if self.__sex == 'м':
            return round(88.362 + 13.397 * w + 4.799 * h - 5.677 * a)
        return round(447.593 + 9.247 * w + 3.098 * h - 4.330 * a)

    # строка для print(): ИМТ, его статус и суточная норма калорий
    def __str__(self):
        return (f'{self.__fio}: ИМТ {self.bmi()} ({self.bmi_status()}), '
                f'норма {self.daily_calories()} ккал/сут')


# создаём четырёх пациентов с разными показателями
people = [
    HealthMetrics('Турусбеков Максат', 178, 72, 30, 'м'),
    HealthMetrics('Майлибаева Нармиля', 165, 48, 24, 'ж'),
    HealthMetrics('Мыктыбеков Айдар', 170, 92, 41, 'м'),
    HealthMetrics('Алиев Ислам', 160, 105, 52, 'ж'),
]
for man in people:
    print(man)

# проверяем валидацию: недопустимый вес вызывает ValueError
try:
    people[0].weight = 1
except ValueError as err:
    print('Ошибка:', err)