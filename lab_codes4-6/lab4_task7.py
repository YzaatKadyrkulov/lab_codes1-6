# Лабораторная работа 4, задание 7. Источники энергии
from abc import ABC, abstractmethod


# Абстрактный базовый класс для всех источников энергии
class EnergySource(ABC):
    # Каждый источник должен рассчитывать выработку энергии и КПД
    @abstractmethod
    def generate(self, hours): ...  # Выработка энергии за период, кВт·ч

    @abstractmethod
    def efficiency(self): ...  # Коэффициент полезного действия (КПД)

    # Общий метод для расчёта годовой выработки энергии
    def annual_output(self):
        return round(self.generate(8760))  # В году 8760 часов


# Класс солнечной панели
class SolarPanel(EnergySource):
    # Среднее количество солнечных часов в сутки для разных регионов
    SUN = {'экватор': 5.5, 'средние широты': 3.8, 'север': 2.5}

    def __init__(self, sq_m, eff_pct, peak_kw, zone):
        self.sq_m, self.eff_pct, self.peak_kw, self.zone = sq_m, eff_pct, peak_kw, zone

    # Рассчитываем выработку с учётом мощности и солнечных часов
    def generate(self, hours):
        return self.peak_kw * self.SUN[self.zone] * hours / 24

    # Переводим КПД из процентов в долю
    def efficiency(self):
        return self.eff_pct / 100


# Класс ветряной турбины
class WindTurbine(EnergySource):
    def __init__(self, wind, rotor_d, tower_h):
        self.wind, self.rotor_d, self.tower_h = wind, rotor_d, tower_h

    # Рассчитываем площадь ротора и мощность ветра
    def generate(self, hours):
        area = 3.14159 * (self.rotor_d / 2) ** 2
        power_kw = 0.5 * 1.2 * area * self.wind ** 3 * 0.4 / 1000
        return power_kw * hours  # Энергия = мощность × время

    # Условный КПД ветряной турбины — 40%
    def efficiency(self):
        return 0.4


# Класс гидроэлектростанции
class HydroPower(EnergySource):
    def __init__(self, head_m, flow, eff):
        self.head_m, self.flow, self.eff = head_m, flow, eff

    # Рассчитываем выработку по напору воды, расходу и КПД
    def generate(self, hours):
        return 9.81 * self.head_m * self.flow * self.eff * hours  # кВт·ч

    def efficiency(self):
        return self.eff


# Класс атомного реактора
class NuclearReactor(EnergySource):
    def __init__(self, mw, eff, load_factor):
        self.mw, self.eff, self.load_factor = mw, eff, load_factor

    # Рассчитываем выработку с учётом мощности и коэффициента загрузки
    def generate(self, hours):
        return self.mw * 1000 * self.load_factor * hours

    def efficiency(self):
        return self.eff


# Создаём список источников энергии с их параметрами
park = [
    SolarPanel(2000, 21, 400, 'средние широты'),
    WindTurbine(9, 90, 100),
    HydroPower(60, 25, 0.88),
    NuclearReactor(1000, 0.33, 0.9),
]

# Выводим КПД и выработку каждого источника за сутки и год
for src in park:
    print(f'{type(src).__name__:<14} КПД {src.efficiency():.0%}  '
          f'за сутки {src.generate(24):>12,.0f} кВт·ч  '
          f'за год {src.annual_output() / 1e6:>8.2f} ГВт·ч'.replace(',', ' '))

# Находим источник с максимальной годовой выработкой
best = max(park, key=lambda s: s.annual_output())
print('Больше всего за год вырабатывает:', type(best).__name__)