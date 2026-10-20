# Лабораторная работа 3, задание 3. Бытовая техника
# родительский класс: общие данные и поведение всех приборов
class Appliance:
    def __init__(self, maker, watts, cost, eclass):
        self.maker = maker                 # бренд
        self.watts = watts                 # мощность, Вт
        self.cost = cost                   # цена, $
        self.eclass = eclass               # класс энергопотребления

    def spec(self):
        return f'{self.maker}: {self.watts} Вт, ${self.cost}, класс {self.eclass}'

    # стоимость энергии = мощность (кВт) × часы × тариф
    def energy_cost(self, hours, rate):
        return round(self.watts / 1000 * hours * rate, 2)

    # compare() определён в родителе и работает для любых двух приборов;
    # внутри вызывается energy_cost(), поэтому у холодильников сработает
    # их переопределённая версия
    def compare(self, other):
        a, b = self.energy_cost(10, 3), other.energy_cost(10, 3)
        word = 'экономичнее' if a < b else 'прожорливее'
        return f'{self.maker} {word}, чем {other.maker} (за 10 ч: {a} и {b} сом)'


# наследование: стиральная машина получает все методы Appliance и дополняет их
class WashingMachine(Appliance):
    def __init__(self, maker, watts, cost, eclass, drum_kg, programs, wash_temp):
        # вызываем конструктор родителя для общих атрибутов
        super().__init__(maker, watts, cost, eclass)
        # атрибуты, которые есть только у стиральной машины
        self.drum_kg, self.programs, self.wash_temp = drum_kg, programs, wash_temp

    # переопределение: расширяем описание родителя через super(), а не копируем его
    def spec(self):
        return (f'{super().spec()} | барабан {self.drum_kg} кг, '
                f'режимов: {len(self.programs)}, до {self.wash_temp}°C')


class Refrigerator(Appliance):
    def __init__(self, maker, watts, cost, eclass, litres, chambers, freezer_temp):
        super().__init__(maker, watts, cost, eclass)
        self.litres, self.chambers, self.freezer_temp = litres, chambers, freezer_temp

    # переопределение: у холодильника своя формула расхода энергии
    def energy_cost(self, hours, rate):
        # компрессор работает примерно треть времени
        return round(super().energy_cost(hours, rate) / 3, 2)

    def spec(self):
        return (f'{super().spec()} | {self.litres} л, камер: {self.chambers}, '
                f'морозилка {self.freezer_temp}°C')


# создаём по две модели каждого вида
wm1 = WashingMachine('LG', 500, 420, 'A+', 8, ['хлопок', 'синтетика', 'быстрая'], 90)
wm2 = WashingMachine('Bosch', 450, 510, 'A++', 7, ['хлопок', 'шерсть'], 60)
fr1 = Refrigerator('Samsung', 150, 650, 'A+', 360, 2, -18)
fr2 = Refrigerator('Atlant', 130, 380, 'A', 280, 2, -15)

# один цикл работает с приборами разных классов (полиморфизм):
# вызовы одинаковые, а считается по правилам конкретного класса
for dev in (wm1, wm2, fr1, fr2):
    print(dev.spec())
    print(f'24 часа работы при тарифе 3 сом/кВт·ч: {dev.energy_cost(24, 3)} сом')

# compare() работает для любых двух приборов
print(wm1.compare(wm2))
print(fr1.compare(fr2))