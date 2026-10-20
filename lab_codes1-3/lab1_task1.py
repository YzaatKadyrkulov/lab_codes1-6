# Лабораторная работа 1, задание 1. Класс «Книга»
CURRENT_YEAR = 2026


class Book:
    category = 'Печатное издание'  # атрибут класса

    def __init__(self, caption, writer, issued, page_total):
        self.caption = caption  # название
        self.writer = writer  # автор
        self.issued = issued  # год издания
        self.page_total = page_total  # число страниц

    def age(self):
        """Возраст книги в годах."""
        return CURRENT_YEAR - self.issued

    def describe(self):
        return (f'«{self.caption}», {self.writer}, '
                f'{self.issued} г., {self.page_total} стр.')

    def is_long_read(self):
        return self.page_total > 400


shelf = [
    Book('Преступление и наказание', 'Фёдор Достоевский', 1866, 671),
    Book('Гарри Поттер', 'Дж. К. Роулинг', 1997, 320),
    Book('Алхимик', 'Пауло Коэльо', 1988, 208),
]
print('Категория:', Book.category)
for item in shelf:
    print(item.describe())
    print('возраст:', item.age(), 'лет')
    print('длинное чтение:', 'да' if item.is_long_read() else 'нет')
