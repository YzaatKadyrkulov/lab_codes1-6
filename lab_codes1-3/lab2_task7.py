# Лабораторная работа 2, задание 7. Класс «Сейф»
class Safe:
    def __init__(self, code, master, stuff):
        # приватные атрибуты (name mangling): снаружи класса напрямую недоступны,
        # поэтому обойти защиту можно только через методы
        self.__pin = code                  # PIN-код владельца
        self.__master = master             # мастер-код для разблокировки
        self.__content = list(stuff)       # копия списка, чтобы внешний список не менял сейф
        self.__attempts = 0                # счётчик неверных попыток
        self.__locked = False              # флаг блокировки

    def open(self, code):
        # сначала проверяем блокировку: заблокированный сейф PIN не принимает
        if self.__locked:
            print('Сейф заблокирован. Нужен мастер-код.')
            return None
        # верный PIN: сбрасываем счётчик и показываем содержимое
        if code == self.__pin:
            self.__attempts = 0
            print('Сейф открыт. Внутри:', ', '.join(self.__content))
            return list(self.__content)    # возвращаем копию, а не сам список
        # неверный PIN: увеличиваем счётчик попыток
        self.__attempts += 1
        print(f'Неверный PIN (попытка {self.__attempts} из 3)')
        # после третьей неудачи блокируем сейф
        if self.__attempts >= 3:
            self.__locked = True
            print('!!! Сейф заблокирован')
        return None

    # положить предмет можно только в незаблокированный сейф и с верным PIN
    def put(self, item, code):
        if not self.__locked and code == self.__pin:
            self.__content.append(item)
            print(f'Положили: {item}')
        else:
            print('Не удалось положить предмет')

    # разблокировать сейф можно только мастер-кодом
    def reset(self, master_pin):
        if master_pin == self.__master:
            # одновременно снимаем блокировку и обнуляем счётчик
            self.__locked, self.__attempts = False, 0
            print('Сейф разблокирован мастер-кодом')
        else:
            print('Неверный мастер-код')


# сценарий: неверные попытки → блокировка → разблокировка → открытие
box = Safe('4821', '000777', ['паспорт', 'флешка'])
box.open('1111')           # неверный PIN, попытка 1
box.open('2222')           # неверный PIN, попытка 2
box.open('3333')           # неверный PIN, попытка 3 → блокировка
box.open('4821')           # уже заблокирован, даже верный PIN не принимается
box.reset('123456')        # неверный мастер-код
box.reset('000777')        # верный мастер-код → сейф разблокирован
box.put('договор', '4821')
box.open('4821')