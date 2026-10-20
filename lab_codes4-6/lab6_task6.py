# Лабораторная работа 6, задание 6. Образовательная платформа


# Singleton: единый каталог курсов
class CourseManager:
    _only = None

    def __new__(cls):
        # Создаём менеджер только один раз
        if cls._only is None:
            cls._only = super().__new__(cls)
            cls._only.catalog = []  # Общий список курсов
        return cls._only


# Класс урока
class Lesson:
    KINDS = ('видео', 'текст', 'тест', 'задание')

    def __init__(self, topic, kind, points):
        # Проверяем, что тип урока допустим
        if kind not in self.KINDS:
            raise ValueError(f'Недопустимый тип урока: {kind}')

        self.topic = topic
        self.kind = kind
        self.points = points


# Студент — агрегация: существует независимо от курса
class Student:
    def __init__(self, fio):
        self.fio = fio
        self.passed = {}  # Тема урока → набранные баллы

    # Наблюдатель: получает уведомление о новом уроке
    def update(self, course, lesson):
        print(
            f'[{self.fio}] новый урок в «{course.name}»: '
            f'{lesson.topic} ({lesson.kind})'
        )

    # Сохраняем результат студента, не превышая максимум баллов
    def complete(self, lesson, score):
        self.passed[lesson.topic] = min(score, lesson.points)


# Курс содержит уроки и список записанных студентов
class Course:
    def __init__(self, name, direction):
        self.name = name
        self.direction = direction
        self._lessons = []  # Композиция: уроки принадлежат курсу
        self._students = []  # Подписанные студенты

    # Подписываем студента на обновления курса
    def subscribe(self, student):
        self._students.append(student)

    # Создаём урок, добавляем в курс и уведомляем студентов
    def publish(self, topic, kind, points):
        lesson = Lesson(topic, kind, points)
        self._lessons.append(lesson)

        # Отправляем уведомление каждому подписанному студенту
        for st in self._students:
            st.update(self, lesson)

        return lesson

    # Рассчитываем прогресс студента по курсу
    def progress(self, student):
        total = sum(l.points for l in self._lessons)
        got = sum(student.passed.get(l.topic, 0) for l in self._lessons)
        done = sum(1 for l in self._lessons if l.topic in student.passed)

        return (
            f'{student.fio}: пройдено {done} из {len(self._lessons)}, '
            f'балл {got / total:.0%}'
        )


# Factory: создаёт курсы по направлению и инструменту
class CourseFactory:
    TITLES = {
        'программирование': 'Основы {}',
        'дизайн': 'Дизайн-мышление: {}',
        'анализ данных': 'Анализ данных на {}'
    }

    @classmethod
    def create(cls, direction, tool):
        # Формируем название и создаём курс
        course = Course(cls.TITLES[direction].format(tool), direction)

        # Добавляем курс в общий каталог
        CourseManager().catalog.append(course)
        return course


# Создаём курсы через фабрику
py = CourseFactory.create('программирование', 'Python')
ux = CourseFactory.create('дизайн', 'интерфейсы')

# Проверяем Singleton и количество курсов
print(
    'Менеджер один:', CourseManager() is CourseManager(),
    '| курсов в каталоге:', len(CourseManager().catalog)
)

# Создаём студентов
s1, s2 = Student('Алмаз Усенов'), Student('Дарья Ли')

# Подписываем студентов на курсы
py.subscribe(s1)
py.subscribe(s2)
ux.subscribe(s2)

# Публикуем уроки по программированию
v = py.publish('Переменные и типы', 'видео', 10)
t = py.publish('Условия и циклы', 'текст', 20)
q = py.publish('Мини-тест', 'тест', 30)

# Публикуем урок по дизайну
ux.publish('Пользовательские сценарии', 'задание', 40)

# Записываем результаты студентов
s1.complete(v, 10)
s1.complete(t, 15)

s2.complete(v, 10)
s2.complete(t, 20)
s2.complete(q, 27)

# Выводим прогресс студентов по курсу Python
print(py.progress(s1))
print(py.progress(s2))