# Лабораторная работа 5, задание 8. Стек (Stack)


# Класс для реализации структуры данных «Стек»
class Stack:
    def __init__(self, data=()):
        self._data = list(data)  # Храним элементы; вершина стека — последний элемент

    # Добавляем элемент на вершину стека
    def push(self, item): self._data.append(item)

    # Удаляем и возвращаем верхний элемент стека
    def pop(self):
        if not self._data:
            raise ValueError('Стек пуст')  # Ошибка, если стек пуст
        return self._data.pop()

    # Просматриваем верхний элемент без удаления
    def peek(self): return self._data[-1]

    # Возвращаем количество элементов
    def __len__(self): return len(self._data)

    # Проверяем, содержится ли элемент в стеке
    def __contains__(self, item): return item in self._data

    # Перебираем элементы от вершины к основанию
    def __iter__(self): return iter(reversed(self._data))

    # Объединяем два стека в новый стек
    def __add__(self, o): return Stack(self._data + o._data)

    # Проверяем равенство содержимого двух стеков
    def __eq__(self, o): return self._data == o._data

    # Проверяем, пустой ли стек
    def __bool__(self): return bool(self._data)

    # Получаем элемент по индексу, начиная с вершины
    def __getitem__(self, i): return self._data[-1 - i]

    # Преобразуем стек в строку, начиная с вершины
    def __str__(self): return ' | '.join(str(x) for x in self)

    # Представление объекта для отладки
    def __repr__(self): return f'Stack({self._data})'


# Функция проверяет правильность расстановки скобок
def brackets_ok(text):
    # Для каждой закрывающей скобки указываем соответствующую открывающую
    pairs = {')': '(', ']': '[', '}': '{'}
    st = Stack()

    # Проверяем каждый символ строки
    for ch in text:
        if ch in '([{':
            st.push(ch)  # Запоминаем открывающую скобку
        elif ch in pairs:
            # Проверяем, есть ли открывающая скобка и совпадает ли её тип
            if not st or st.pop() != pairs[ch]:
                return False

    # Если стек пуст, все скобки закрыты правильно
    return not st


# Создаём стек и добавляем в него названия книг
s = Stack()
for book in ['Python', 'Алгоритмы', 'Сети', 'Базы данных']:
    s.push(book)

# Выводим стек, количество элементов и проверяем доступ к элементам
print('стек (вершина слева):', s, '| repr:', repr(s))
print('len =', len(s), '| peek =', s.peek(), '| s[1] =', s[1], '| "Сети" in s:', 'Сети' in s)

# Удаляем верхнюю книгу и выводим обновлённый стек
print('pop ->', s.pop(), '| после pop:', s)

# Создаём второй стек и проверяем объединение и сравнение
t = Stack([10, 20])
print('s + t =', s + t, '| s == s + Stack():', s == s + Stack(), '| bool(Stack()) =', bool(Stack()))

# Проверяем перебор элементов второго стека
print('итерация:', [item for item in t])

# Проверяем обработку ошибки при удалении из пустого стека
try:
    Stack().pop()
except ValueError as err:
    print('Ошибка:', err)

# Проверяем правильность скобок в разных выражениях
for expr in ['{[(2+3)*4]-1}', '((a+b)*c', '[(])', 'f(x[i]) + {y}']:
    print(f'{expr:<16} скобки расставлены верно: {brackets_ok(expr)}')