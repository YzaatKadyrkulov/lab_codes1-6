# Лабораторная работа 4, задание 1. Космические аппараты
from abc import ABC, abstractmethod


# абстрактный базовый класс: задаёт обязательный интерфейс для всех аппаратов
# (наследуем от ABC, поэтому создать объект этого класса нельзя)
class Spacecraft(ABC):
    def __init__(self, craft_name):
        self.craft_name = craft_name       # название аппарата

    # каждый наследник обязан реализовать эти три метода,
    # иначе создать его объект не получится (будет TypeError)
    @abstractmethod
    def launch(self): ...

    @abstractmethod
    def mission_description(self): ...

    @abstractmethod
    def fuel_consumption(self, distance_km): ...


class Satellite(Spacecraft):
    def __init__(self, craft_name, orbit_alt, rev_minutes, role):
        # вызываем конструктор родителя для общего атрибута
        super().__init__(craft_name)
        # орбита (км), период обращения (мин), назначение
        self.orbit_alt, self.rev_minutes, self.role = orbit_alt, rev_minutes, role

    def launch(self):
        return f'Спутник «{self.craft_name}» выведен на орбиту {self.orbit_alt} км'

    def mission_description(self):
        return f'назначение: {self.role}, виток за {self.rev_minutes} мин'

    # у спутника расход топлива небольшой: 0,02 на каждый км
    def fuel_consumption(self, distance_km):
        return round(distance_km * 0.02, 1)


class SpaceStation(Spacecraft):
    def __init__(self, craft_name, crew, blocks, life_years, tests):
        super().__init__(craft_name)
        # экипаж, число модулей, срок службы, список экспериментов
        self.crew, self.blocks, self.life_years, self.tests = crew, blocks, life_years, tests

    def launch(self):
        return f'Станция «{self.craft_name}» собрана из {self.blocks} модулей'

    def mission_description(self):
        return f'экипаж {self.crew} чел., экспериментов: {len(self.tests)}'

    # у станции расход зависит ещё и от размера экипажа
    def fuel_consumption(self, distance_km):
        return round(distance_km * 0.5 + self.crew * 10, 1)


class Rover(Spacecraft):
    def __init__(self, craft_name, planet, speed, energy, passed_km):
        super().__init__(craft_name)
        # планета, скорость (км/ч), источник энергии, пройденный путь (км)
        self.planet, self.speed, self.energy, self.passed_km = planet, speed, energy, passed_km

    def launch(self):
        return f'Ровер «{self.craft_name}» совершил посадку, планета: {self.planet}'

    def mission_description(self):
        return f'источник энергии: {self.energy}, пройдено {self.passed_km} км'

    # солнечному роверу топливо не нужно, остальным — минимальный расход
    def fuel_consumption(self, distance_km):
        return 0.0 if self.energy == 'солнечный' else round(distance_km * 0.001, 3)


class Probe(Spacecraft):
    def __init__(self, craft_name, target, dist_mln, working):
        super().__init__(craft_name)
        # цель, расстояние (млн км), активна ли
        self.target, self.dist_mln, self.working = target, dist_mln, working

    def launch(self):
        return f'Зонд «{self.craft_name}» стартовал к цели: {self.target}'

    def mission_description(self):
        state = 'активен' if self.working else 'работа завершена'
        return f'расстояние {self.dist_mln} млн км, {state}'

    def fuel_consumption(self, distance_km):
        return round(distance_km * 0.08, 1)


# создать абстрактный класс напрямую нельзя: будет TypeError
try:
    Spacecraft('тест')
except TypeError as err:
    print('Абстрактный класс не создать:', err)

# по одному аппарату каждого типа в одном списке
fleet = [
    Satellite('Курс-1', 550, 95, 'связь'),
    SpaceStation('Орбита-М', 6, 9, 15, ['биология', 'материалы', 'медицина']),
    Rover('Ала-Тоо', 'Марс', 0.14, 'солнечный', 18.5),
    Probe('Дальний', 'комета', 420, True),
]

# полиморфизм: одни и те же вызовы для аппаратов разных типов,
# а выполняется реализация того класса, к которому относится объект
for craft in fleet:
    print(craft.launch())
    print(f'{craft.mission_description()}; топливо на 1000 км: {craft.fuel_consumption(1000)}')