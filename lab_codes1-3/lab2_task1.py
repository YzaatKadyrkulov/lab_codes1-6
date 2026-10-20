# Лабораторная работа 2, задание 1. Класс «Банковский счёт»
class BankAccount:
    def __init__(self, holder, opening=0):
        # двойное подчёркивание: атрибуты приватные (name mangling),
        # снаружи класса к ним нельзя обратиться напрямую
        self.__owner = holder
        self.__balance = opening
        self.__log = [f'Открытие счёта: {opening} сом']   # журнал операций

    # свойство только для чтения: сеттера нет, баланс меняют лишь методы класса
    @property
    def balance(self):                       # только чтение
        return self.__balance

    def deposit(self, money):
        # пополнение допустимо только на положительную сумму
        if money <= 0:
            print('Ошибка: сумма пополнения должна быть положительной')
            return False
        self.__balance += money
        self.__log.append(f'Пополнение: +{money} сом')   # фиксируем операцию
        return True

    def withdraw(self, money):
        # нельзя снять неположительную сумму или больше остатка на счёте
        if money <= 0 or money > self.__balance:
            print(f'Отказ: снятие {money} сом невозможно')
            return False
        self.__balance -= money
        self.__log.append(f'Снятие: -{money} сом')
        return True

    # выписка: история операций и текущий баланс одной строкой
    def get_statement(self):
        lines = [f'Выписка по счёту: {self.__owner}']
        # enumerate нумерует операции, начиная с 1
        lines += [f'{n}. {rec}' for n, rec in enumerate(self.__log, 1)]
        lines.append(f'Текущий баланс: {self.__balance} сом')
        return '\n'.join(lines)


# первый счёт: 5 операций, среди них две заведомо неверные
first = BankAccount('Бексултан Сабырбеков', 12000)
first.deposit(3500)
first.withdraw(5000)
first.withdraw(20000)          # больше остатка
first.deposit(-100)            # неверная сумма
first.withdraw(2500)
print(first.get_statement())
print()

# второй счёт открывается с нулевым балансом (значение по умолчанию)
second = BankAccount('Совхозова Сабина')
second.deposit(8000)
second.withdraw(1200)
second.deposit(450)
second.withdraw(0)             # нулевая сумма — отказ
second.deposit(1000)
print(second.get_statement())

# проверяем инкапсуляцию: прямая запись в balance невозможна
try:
    second.balance = 1_000_000
except AttributeError as err:
    print('\nПопытка записи в balance:', err)