# Лабораторная работа 4, задание 2. Медицинский персонал
from abc import ABC, abstractmethod


# Абстрактный базовый класс для всех медицинских работников
class MedicalWorker(ABC):
    def __init__(self, fio, area):
        self.fio = fio
        self.area = area

    # Абстрактные методы: каждый дочерний класс должен их реализовать
    @abstractmethod
    def treat(self, patient): ...

    @abstractmethod
    def prescribe(self): ...

    @abstractmethod
    def calculate_workload(self): ...  # Рассчитывает загрузку в процентах

    # Формирует карточку работника с его должностью и нагрузкой
    def card(self):
        return f'{type(self).__name__:<11} {self.fio:<20} нагрузка {self.calculate_workload():>5.1f}%'


# Класс врача-терапевта
class Therapist(MedicalWorker):
    def __init__(self, fio, area, visits_day, exp):
        super().__init__(fio, area)  # Передаём ФИО и отделение родительскому классу
        self.visits_day, self.exp = visits_day, exp

    def treat(self, patient):
        return f'{self.fio} осматривает пациента {patient}'

    def prescribe(self):
        return 'назначает анализы и лекарства'

    def calculate_workload(self):
        return self.visits_day / 24 * 100  # Нагрузка зависит от числа приёмов в день


# Класс врача-хирурга
class Surgeon(MedicalWorker):
    def __init__(self, fio, area, ops_month, category):
        super().__init__(fio, area)
        self.ops_month, self.category = ops_month, category

    def treat(self, patient):
        return f'{self.fio} оперирует пациента {patient}'

    def prescribe(self):
        return 'назначает послеоперационный режим'

    def calculate_workload(self):
        return self.ops_month / 20 * 100  # Нагрузка зависит от числа операций в месяц


# Класс медицинской сестры
class Nurse(MedicalWorker):
    # Коэффициенты нагрузки в зависимости от смены
    SHIFT_K = {'дневная': 1.0, 'ночная': 1.2, 'суточная': 1.5}

    def __init__(self, fio, area, shift, patients):
        super().__init__(fio, area)
        self.shift, self.patients = shift, patients

    def treat(self, patient):
        return f'{self.fio} делает пациенту {patient} инъекцию'

    def prescribe(self):
        return 'ничего не назначает, выполняет назначения врачей'

    def calculate_workload(self):
        # Рассчитываем нагрузку с учётом смены, но не более 100%
        return min(100, self.patients * 6 * self.SHIFT_K[self.shift])


# Класс фармацевта
class Pharmacist(MedicalWorker):
    def __init__(self, fio, area, shift, controlled):
        super().__init__(fio, area)
        self.shift, self.controlled = shift, controlled

    def treat(self, patient):
        return f'{self.fio} выдаёт лекарства пациенту {patient}'

    def prescribe(self):
        # Показываем количество препаратов, отпускаемых по рецепту
        return f'отпускает по рецепту, контролируемых позиций: {len(self.controlled)}'

    def calculate_workload(self):
        return 40 + len(self.controlled) * 5  # Базовая нагрузка плюс контролируемые препараты


# Создаём список медицинских работников разных специальностей
staff = [
    Therapist('Абдрахманова Н.', 'терапия', 18, 12),
    Surgeon('Сулайманов Б.', 'хирургия', 14, 'высшая'),
    Nurse('Ким Е.', 'хирургия', 'ночная', 9),
    Pharmacist('Исмаилов Т.', 'аптека', 'дневная', ['морфин', 'кодеин']),
]

# Выводим карточку, действие и назначения каждого работника
for w in staff:
    print(w.card())
    print('   ', w.treat('Асанов'), '|', w.prescribe())

# Вычисляем среднюю нагрузку всего медицинского персонала
mean = sum(w.calculate_workload() for w in staff) / len(staff)
print(f'Средняя нагрузка по отделению: {mean:.1f}%')