# Лабораторная работа 6, задание 7. Гостиница


# Singleton: единый реестр всех отелей сети
class HotelChain:
    _only = None

    def __new__(cls):
        # Создаём объект сети только один раз
        if cls._only is None:
            cls._only = super().__new__(cls)
            cls._only.hotels = []  # Общий список отелей
        return cls._only


# Наблюдатель: ресепшен получает уведомления о состоянии номера
class Reception:
    def update(self, room, state):
        print(f'[Ресепшен] номер {room.number} ({room.kind}): {state}')


# Наблюдатель: служба уборки реагирует на необходимость уборки
class HousekeepingService:
    def update(self, room, state):
        if state == 'убирается':
            print(f'[Горничные] убрать номер {room.number}')


# Гость — агрегация: существует независимо от бронирования
class Guest:
    def __init__(self, fio):
        self.fio = fio


# Бронирование номера
class Booking:
    def __init__(self, guest, check_in, check_out, rate):
        self.guest = guest
        self.check_in = check_in
        self.check_out = check_out

        # Рассчитываем стоимость проживания по количеству дней
        self.cost = (check_out - check_in) * rate


# Номер гостиницы
class Room:
    def __init__(self, number, kind, rate):
        self.number = number
        self.kind = kind
        self.rate = rate
        self.state = 'свободен'

        self._bookings = []  # Композиция: бронирования хранятся в номере
        self._watchers = [Reception(), HousekeepingService()]

    # Изменяем состояние номера и уведомляем наблюдателей
    def set_state(self, state):
        self.state = state

        for w in self._watchers:
            w.update(self, state)

    # Создаём бронирование для гостя
    def book(self, guest, d_in, d_out):
        self._bookings.append(Booking(guest, d_in, d_out, self.rate))

    # Находим бронирования, действующие в указанный день
    def booked_on(self, day):
        return [
            b for b in self._bookings
            if b.check_in <= day < b.check_out
        ]


# Factory: создаёт номера с ценой по типу
class RoomFactory:
    RATES = {
        'стандарт': 3000,
        'полулюкс': 4800,
        'люкс': 7500,
        'апартаменты': 11000
    }

    @classmethod
    def create(cls, number, kind):
        # Создаём номер с соответствующей стоимостью за сутки
        return Room(number, kind, cls.RATES[kind])


# Гостиница
class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = []  # Список номеров гостиницы

        # Регистрируем гостиницу в общей сети
        HotelChain().hotels.append(self)

    # Добавляем номер в гостиницу
    def add_room(self, number, kind):
        room = RoomFactory.create(number, kind)
        self.rooms.append(room)
        return room

    # Формируем отчёт о занятости и выручке за день
    def daily_report(self, day):
        busy = [r for r in self.rooms if r.booked_on(day)]

        # Считаем выручку по суточным тарифам занятых номеров
        income = sum(r.rate for r in busy)

        print(
            f'Отчёт «{self.name}» за день {day}: '
            f'занято {len(busy)} из {len(self.rooms)} '
            f'({len(busy) / len(self.rooms):.0%}), '
            f'выручка {income} сом'
        )


# Создаём гостиницы сети
hotel = Hotel('Ала-Тоо Резорт')
Hotel('Иссык-Куль Бриз')

# Добавляем номера разных категорий
r1 = hotel.add_room(101, 'стандарт')
r2 = hotel.add_room(205, 'полулюкс')
r3 = hotel.add_room(310, 'люкс')
r4 = hotel.add_room(401, 'апартаменты')

# Создаём гостей
g1, g2, g3 = (
    Guest('Тимур Рахимов'),
    Guest('Анна Петрова'),
    Guest('Бакыт Тологонов')
)

# Регистрируем бронирования: день заезда включён, выезда — нет
r1.book(g1, 10, 13)
r2.book(g2, 11, 12)
r3.book(g3, 9, 14)

# Проверяем Singleton и количество отелей в сети
print(
    'Сеть одна:', HotelChain() is HotelChain(),
    '| отелей в сети:', len(HotelChain().hotels)
)

# Изменяем состояния номеров — наблюдатели реагируют на изменения
r1.set_state('занят')
r2.set_state('занят')
r2.set_state('убирается')
r4.set_state('на ремонте')

# Выводим отчёты за 11-й и 13-й дни
hotel.daily_report(11)
hotel.daily_report(13)