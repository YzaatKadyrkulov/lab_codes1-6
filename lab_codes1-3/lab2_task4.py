# Лабораторная работа 2, задание 4. Класс «Электронный кошелёк»
class EWallet:
    def __init__(self, holder, money, cur, one_time_max):
        # приватные атрибуты (name mangling): снаружи класса напрямую недоступны
        self.__holder = holder
        self.__money = money
        self.__cur = cur
        self.__one_time_max = one_time_max   # максимум одного перевода

    # баланс только для чтения: сеттера нет, изменить его можно лишь через методы
    @property
    def balance(self):
        return self.__money

    # вычисляемое свойство: перевод возможен, только если на счёте есть деньги
    @property
    def can_transfer(self):
        return self.__money > 0

    # служебный метод зачисления: одинарное подчёркивание значит «для внутреннего
    # использования», его вызывает transfer() у кошелька-получателя
    def _receive(self, amount):
        self.__money += amount

    def transfer(self, recipient, amount):
        # цепочка проверок: тип получателя, сумма, лимит, остаток на счёте
        if not isinstance(recipient, EWallet):
            print('  Ошибка: получатель не является кошельком')
        elif amount <= 0:
            print('  Ошибка: сумма должна быть положительной')
        elif amount > self.__one_time_max:
            print(f'  Отказ: лимит одного перевода {self.__one_time_max} {self.__cur}')
        elif amount > self.__money:
            print(f'  Отказ: недостаточно средств ({self.__money} {self.__cur})')
        else:
            # все проверки пройдены: списываем у себя и зачисляем получателю
            self.__money -= amount
            recipient._receive(amount)
            print(f'  {self.__holder} → {recipient.__holder}: {amount} {self.__cur}')

    # строка для print(): владелец и остаток
    def __str__(self):
        return f'{self.__holder}: {self.__money} {self.__cur}'


# создаём три кошелька и проводим переводы разных видов
w1 = EWallet('Нурсултан', 5000, 'KGS', 3000)
w2 = EWallet('Айсалкын', 800, 'KGS', 1000)
w3 = EWallet('Руслан', 0, 'KGS', 2000)
w1.transfer(w2, 2000)                      # успешный перевод
w2.transfer(w3, 1500)                      # выше лимита
w2.transfer(w3, 900)                       # успешный перевод
w3.transfer(w1, 1200)                      # недостаточно средств
w1.transfer('Айдар', 100)                  # неверный получатель

# итоговое состояние всех кошельков
for w in (w1, w2, w3):
    print(w, '| можно переводить:', w.can_transfer)