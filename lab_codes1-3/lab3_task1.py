# Лабораторная работа 3, задание 1. Сотрудники компании
# родительский (базовый) класс: общие данные и поведение всех сотрудников
class Employee:
    def __init__(self, fio, post, wage, seniority):
        self.fio = fio
        self.post = post
        self.wage = wage                   # базовая зарплата
        self.seniority = seniority         # стаж, лет

    def salary(self):
        # базовая формула: +2% к базе за каждый год стажа
        return self.wage * (1 + 0.02 * self.seniority)

    def introduce(self):
        return f'{self.fio}, {self.post}, стаж {self.seniority} г.'


# наследование: Manager получает все атрибуты и методы Employee и дополняет их
class Manager(Employee):
    def __init__(self, fio, wage, seniority, dept, crew, bonus_pct):
        # вызываем конструктор родителя, чтобы инициализировать общие атрибуты
        super().__init__(fio, 'менеджер', wage, seniority)
        # атрибуты, которые есть только у менеджера
        self.dept = dept
        self.crew = crew                   # число подчинённых
        self.bonus_pct = bonus_pct         # бонус, % от базовой зарплаты

    # переопределение метода: расширяем расчёт родителя через super(), а не копируем его
    def salary(self):
        return super().salary() + self.wage * self.bonus_pct / 100

    def introduce(self):
        return f'{super().introduce()}; отдел «{self.dept}», подчинённых: {self.crew}'


class Developer(Employee):
    # надбавка к зарплате по уровню разработчика, %
    EXTRA = {'junior': 0, 'middle': 30, 'senior': 60}

    def __init__(self, fio, wage, seniority, lang, grade):
        # вызываем конструктор родителя
        super().__init__(fio, 'разработчик', wage, seniority)
        self.lang = lang                   # язык программирования
        self.grade = grade                 # уровень: junior / middle / senior

    # переопределение: к зарплате родителя добавляется надбавка за уровень
    def salary(self):
        return super().salary() * (1 + self.EXTRA[self.grade] / 100)

    def introduce(self):
        return f'{super().introduce()}; {self.lang}, {self.grade}'


# команда из 6 человек: объекты трёх разных классов в одном списке
staff = [
    Manager('Кучеренко Сергей', 90000, 8, 'Продажи', 12, 25),
    Manager('Кенжебаева Чолпон', 85000, 5, 'Маркетинг', 7, 15),
    Developer('Акылбеков Данияр', 70000, 1, 'Python', 'junior'),
    Developer('Кылычбекова Мээрим', 75000, 4, 'Java', 'middle'),
    Developer('Кадыркулов Ызаат', 80000, 9, 'C++', 'senior'),
    Employee('Ибраимова Назгуль', 'бухгалтер', 50000, 3),
]

# полиморфный цикл: salary() и introduce() вызываются у объектов разных классов
# одинаково, а выполняется версия, соответствующая типу объекта
fund = 0
for person in staff:
    print(person.introduce())
    # формат :,.0f ставит разделитель тысяч, затем заменяем запятую на пробел
    print(f'зарплата: {person.salary():,.0f} сом'.replace(',', ' '))
    fund += person.salary()                # накапливаем зарплатный фонд
print(f'Зарплатный фонд: {fund:,.0f} сом'.replace(',', ' '))

# issubclass проверяет, что один класс является наследником другого
print('Developer — потомок Employee:', issubclass(Developer, Employee))