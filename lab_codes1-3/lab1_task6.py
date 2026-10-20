# Лабораторная работа 1, задание 6. Класс «Студент»
class Student:
    # атрибут класса: общий для всех студентов, хранится один раз
    institution = 'КГТУ им. И. Раззакова'

    # конструктор: вызывается автоматически при создании объекта
    def __init__(self, fio, team, course, mark):
        # атрибуты экземпляра: у каждого студента свои значения
        self.fio = fio
        self.team = team
        self.course = course
        self.mark = mark                   # средний балл 0.0–4.0

    # метод экземпляра: self даёт доступ к данным конкретного студента
    def introduce(self):
        # к атрибуту класса обращаемся через имя класса
        return (f'{self.fio}, группа {self.team}, {self.course} курс, '
                f'{Student.institution}')

    # статус определяется по порогам среднего балла (от высшего к низшему)
    def academic_status(self):
        if self.mark >= 3.5:
            return 'Отличник'
        if self.mark >= 2.5:
            return 'Хорошист'
        if self.mark >= 1.5:
            return 'Удовлетворительно'
        return 'Задолженность'

    # base — параметр со значением по умолчанию (базовая стипендия)
    def scholarship(self, base=3000):
        # размер стипендии зависит от результата academic_status()
        status = self.academic_status()
        if status == 'Отличник':
            return base * 1.5              # отличникам — повышенная
        if status == 'Хорошист':
            return base                    # хорошистам — базовая
        return 0                           # остальным стипендия не назначается


# создаём три объекта одного класса с разными данными
group = [
    Student('Толкунов Адилет', 'ИИ(б)-2-25', 2, 3.8),
    Student('Кадыркулов Ызаат', 'ИИ(б)-1-25', 2, 2.7),
    Student('Сабырбеков Бексултан', 'ИИ(б)-2-25', 2, 1.2),
]

# вызываем методы у каждого объекта в цикле
for man in group:
    print(man.introduce())
    print(f'статус: {man.academic_status()}, стипендия: {man.scholarship()} сом')