# Лабораторная работа 6, задание 2. Библиотека

FINE_PER_DAY = 10  # Штраф за каждый день просрочки, сом


# Singleton: общий каталог книг для всех библиотек
class LibraryCatalog:
    _only = None

    def __new__(cls):
        # Создаём каталог только один раз
        if cls._only is None:
            cls._only = super().__new__(cls)
            cls._only.items = []  # Общий список книг
        return cls._only


# Класс книги
class Book:
    def __init__(self, caption, genre, loan_days):
        self.caption, self.genre, self.loan_days = caption, genre, loan_days
        self.holder, self.due_day = None, None  # Читатель и срок возврата


# Factory: создаёт книги со сроком выдачи в зависимости от жанра
class BookFactory:
    DAYS = {'классика': 30, 'наука': 21, 'детектив': 14, 'новинка': 7}

    @classmethod
    def create(cls, caption, genre):
        # Создаём книгу с подходящим сроком выдачи
        return Book(caption, genre, cls.DAYS[genre])


# Наблюдатель: читатель получает уведомления о книгах и штрафах
# Читатель существует независимо от библиотеки
class Reader:
    def __init__(self, fio):
        self.fio, self.debt = fio, 0  # ФИО и сумма долга

    def update(self, text):
        print(f'[Читатель {self.fio}] {text}')


# Наблюдатель: библиотекарь получает уведомления об операциях
class Librarian:
    def update(self, text):
        print(f'[Библиотекарь] {text}')


# Класс библиотеки
class Library:
    def __init__(self, hall):
        self.hall = hall
        self._books = []  # Композиция: библиотека хранит свои книги
        self._readers = []  # Агрегация: читатели существуют отдельно
        self._staff = Librarian()  # Создаём библиотекаря

    # Добавляем книгу в библиотеку и общий каталог
    def add_book(self, caption, genre):
        book = BookFactory.create(caption, genre)
        self._books.append(book)
        LibraryCatalog().items.append(book)
        return book

    # Регистрируем читателя в библиотеке
    def join(self, reader):
        self._readers.append(reader)

    # Выдаём книгу читателю и устанавливаем срок возврата
    def issue(self, book, reader, today):
        book.holder, book.due_day = reader, today + book.loan_days
        reader.update(f'вам выдана «{book.caption}», вернуть до дня {book.due_day}')
        self._staff.update(f'выдана «{book.caption}» ({reader.fio})')

    # Принимаем книгу и рассчитываем штраф за просрочку
    def take_back(self, book, today):
        late = max(0, today - book.due_day)  # Количество дней просрочки
        fine = late * FINE_PER_DAY  # Размер штрафа
        reader = book.holder
        reader.debt += fine  # Добавляем штраф к долгу читателя
        book.holder = book.due_day = None  # Освобождаем книгу
        reader.update(f'«{book.caption}» возвращена, просрочка {late} дн., штраф {fine} сом')
        self._staff.update(f'принята «{book.caption}»')


# Создаём библиотеку и добавляем книги разных жанров
lib = Library('Читальный зал №2')
b1 = lib.add_book('Война и мир', 'классика')
b2 = lib.add_book('Краткая история времени', 'наука')
b3 = lib.add_book('Дело о пропавшем кыргызском манускрипте', 'детектив')
b4 = lib.add_book('Сборник 2026 года', 'новинка')

# Создаём читателей и регистрируем их в библиотеке
r1, r2 = Reader('Айжан Калыкова'), Reader('Нурбек Эсенов')
lib.join(r1)
lib.join(r2)

# Проверяем Singleton и количество книг в общем каталоге
print('Книг в общем каталоге:', len(LibraryCatalog().items),
      '| каталог один:', LibraryCatalog() is LibraryCatalog())

# Выдаём книги читателям в первый день
lib.issue(b1, r1, today=1)
lib.issue(b4, r2, today=1)

# Принимаем книги обратно и рассчитываем возможные штрафы
lib.take_back(b1, today=25)  # Возврат в срок, штрафа нет
lib.take_back(b4, today=14)  # Просрочка 6 дней, штраф 60 сом

# Выводим итоговую задолженность читателей
print(f'Долг {r1.fio}: {r1.debt} сом; долг {r2.fio}: {r2.debt} сом')