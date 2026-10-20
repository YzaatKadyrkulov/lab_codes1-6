# Лабораторная работа 6, задание 8. Транспортный парк


# Singleton: единый реестр всего транспорта
class FleetManager:
    _only = None

    def __new__(cls):
        # Создаём менеджер только один раз
        if cls._only is None:
            cls._only = super().__new__(cls)
            cls._only.vehicles = []  # Общий список транспорта
        return cls._only


# Наблюдатель: диспетчер получает уведомления об изменении статуса
class Dispatcher:
    def update(self, veh, status):
        print(f'   [Диспетчер] {veh.plate} ({veh.kind}): {status}')


# Наблюдатель: сервисный центр реагирует на ремонт
class ServiceCenter:
    def update(self, veh, status):
        if status == 'в ремонте':
            print(f'[Сервис] принять {veh.plate} на обслуживание')


# Водитель — агрегация: существует независимо от автомобиля
class Driver:
    def __init__(self, fio):
        self.fio = fio


# Запись о техническом обслуживании транспорта
class MaintenanceRecord:
    def __init__(self, day, work, price):
        self.day = day
        self.work = work
        self.price = price


# Базовый класс транспортного средства
class Vehicle:
    STATUSES = ('на маршруте', 'в ремонте', 'на стоянке', 'списан')

    def __init__(self, plate, kind, seats):
        self.plate = plate
        self.kind = kind
        self.seats = seats
        self.status = 'на стоянке'
        self.mileage = 0  # Начальный пробег

        self._records = []  # Композиция: записи о ремонте хранятся внутри
        self.drivers = []  # Водители передаются извне
        self._watchers = [Dispatcher(), ServiceCenter()]

        # Автоматически регистрируем транспорт в общем реестре
        FleetManager().vehicles.append(self)

    # Назначаем водителя на транспорт
    def assign(self, driver):
        self.drivers.append(driver)

    # Добавляем запись о техническом обслуживании
    def service(self, day, work, price):
        self._records.append(MaintenanceRecord(day, work, price))

    # Считаем общие расходы на обслуживание транспорта
    def expenses(self):
        return sum(r.price for r in self._records)

    # Меняем статус и уведомляем наблюдателей
    def set_status(self, status):
        if status not in self.STATUSES:
            raise ValueError(f'Неизвестный статус: {status}')

        self.status = status

        # Отправляем уведомление каждому наблюдателю
        for w in self._watchers:
            w.update(self, status)


# Класс автобуса
class Bus(Vehicle):
    pass


# Класс маршрутки
class Minibus(Vehicle):
    pass


# Класс грузовика
class Truck(Vehicle):
    pass


# Класс легкового автомобиля
class Car(Vehicle):
    pass


# Factory: создаёт транспорт с заданным количеством мест
class VehicleFactory:
    kinds = {
        'автобус': (Bus, 45),
        'маршрутка': (Minibus, 18),
        'грузовик': (Truck, 2),
        'легковой': (Car, 4)
    }

    @classmethod
    def create(cls, kind, plate):
        # Получаем класс транспорта и количество мест
        klass, seats = cls.kinds[kind]

        # Создаём объект нужного класса
        return klass(plate, kind, seats)


# Формируем общий отчёт по транспортному парку
def fleet_report():
    fleet = FleetManager().vehicles

    # Считаем количество транспорта на маршруте
    on_route = sum(1 for v in fleet if v.status == 'на маршруте')

    # Выводим количество транспорта, расходы и общий пробег
    print(
        f'Транспорта: {len(fleet)}; '
        f'расходы на обслуживание: {sum(v.expenses() for v in fleet)} сом; '
        f'пробег: {sum(v.mileage for v in fleet)} км'
    )

    # Рассчитываем долю транспорта, который используется
    print(
        f'КПД использования парка: {on_route / len(fleet):.0%} '
        f'({on_route} из {len(fleet)} на маршруте)'
    )


# Создаём водителей
d1, d2, d3 = (
    Driver('Кубанычбек А.'),
    Driver('Рустам Н.'),
    Driver('Эмиль Т.')
)

# Создаём транспорт через фабрику
v1 = VehicleFactory.create('автобус', '01KG 123 ABC')
v2 = VehicleFactory.create('маршрутка', '01KG 777 BCD')
v3 = VehicleFactory.create('грузовик', '01KG 405 EKA')
v4 = VehicleFactory.create('легковой', '01KG 088 DDA')

# Назначаем водителей на транспорт
# Один водитель может работать на нескольких машинах
for veh, drv in [
    (v1, d1),
    (v2, d1),
    (v2, d2),
    (v3, d3),
    (v4, d2)
]:
    veh.assign(drv)

# Проверяем Singleton и количество единиц транспорта
print(
    'Менеджер один:', FleetManager() is FleetManager(),
    '| единиц транспорта:', len(FleetManager().vehicles)
)

# Выводим автобус на маршрут и указываем пробег
v1.set_status('на маршруте')
v1.mileage = 420

# Выводим маршрутку на маршрут и указываем пробег
v2.set_status('на маршруте')
v2.mileage = 310

# Отправляем грузовик на ремонт и записываем расходы
v3.set_status('в ремонте')
v3.service(5, 'замена тормозных колодок', 8500)
v3.service(9, 'масло и фильтры', 3200)

# Записываем расходы на обслуживание легкового автомобиля
v4.service(3, 'шиномонтаж', 1500)

# Меняем статус автомобиля на списанный
v4.set_status('списан')

# Выводим итоговый отчёт по транспортному парку
fleet_report()