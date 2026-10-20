# Лабораторная работа 2, задание 5. Класс «Пароль»
class SecurePassword:
    def __init__(self):
        # приватные атрибуты (name mangling): снаружи класса напрямую недоступны
        self.__password = None             # принятый пароль (None, пока не задан)
        self.__last_try = ''               # последняя попытка, нужна для strength()

    # статический метод: не использует self, только проверяет текст пароля
    # и возвращает список нарушений
    @staticmethod
    def _problems(text):
        found = []
        if len(text) < 8:
            found.append('длина меньше 8 символов')
        # any() истинно, если хотя бы один символ подходит под условие
        if not any(ch.isdigit() for ch in text):
            found.append('нет ни одной цифры')
        if not any(ch.isupper() for ch in text):
            found.append('нет заглавной буквы')
        if ' ' in text:
            found.append('содержит пробелы')
        return found

    # геттер: пароль наружу не отдаём, возвращаем только маску из звёздочек
    @property
    def password(self):
        return '*' * len(self.__password) if self.__password else None

    # сеттер: принимает пароль, только если нет ни одного нарушения
    @password.setter
    def password(self, text):
        self.__last_try = text
        problems = self._problems(text)
        for item in problems:              # каждое нарушение выводим отдельно
            print(f'   ✗ {item}')
        if not problems:
            self.__password = text
            print('✓ пароль принят')

    # сравнение введённого текста с сохранённым паролем
    def check(self, text):
        return self.__password == text

    # надёжность = число выполненных условий из четырёх
    def strength(self):
        ok = 4 - len(self._problems(self.__last_try))
        return 'Сильный' if ok == 4 else 'Средний' if ok == 3 else 'Слабый'


# каждый пароль тестируем на новом объекте
for pwd in ['qwerty', 'Bishkek2026', 'abc 12', 'Ala-Too_777', 'ПАРОЛЬ']:
    obj = SecurePassword()
    print(f'Пароль «{pwd}»:')
    obj.password = pwd                     # вызывается сеттер
    print(f'надёжность: {obj.strength()}, check: {obj.check(pwd)}, '
          f'хранится: {obj.password}')