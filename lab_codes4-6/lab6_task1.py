# Лабораторная работа 6, задание 1. Умный дом

# Singleton: единый контроллер и общий реестр устройств
class HomeController:
    _only = None

    def __new__(cls):
        # Создаём только один экземпляр контроллера
        if cls._only is None:
            cls._only = super().__new__(cls)
            cls._only.registry = []  # Список всех зарегистрированных устройств
        return cls._only

    # Добавляем устройство в общий реестр
    def register(self, dev):
        self.registry.append(dev)


# Наблюдатель: получает уведомления об изменении состояния устройств
class Owner:
    def update(self, dev, event):
        print(f'[Владелец] {dev.label}: {event}')


# Наблюдатель: получает уведомления о событиях безопасности
class SecurityService:
    def update(self, dev, event):
        # Реагируем только на замки и камеры
        if isinstance(dev, (SecurityLock, Camera)):
            print(f'[Охрана] зафиксировано: {dev.label} — {event}')


# Базовый класс всех устройств умного дома
class Device:
    def __init__(self, label, room):
        self.label, self.room, self.state = label, room, 'выкл'
        self._watchers = []  # Список наблюдателей устройства

    # Подписываем наблюдателя на уведомления
    def subscribe(self, watcher):
        self._watchers.append(watcher)

    # Меняем состояние устройства и уведомляем наблюдателей
    def set_state(self, new_state):
        self.state = new_state
        for w in self._watchers:
            w.update(self, f'состояние → {new_state}')


# Конкретные типы устройств наследуются от Device
class Lamp(Device): pass
class Thermostat(Device): pass
class SecurityLock(Device): pass
class Camera(Device): pass


# Factory: создаёт устройства нужного типа
class DeviceFactory:
    kinds = {
        'lamp': Lamp,
        'thermostat': Thermostat,
        'lock': SecurityLock,
        'camera': Camera
    }

    @classmethod
    def create(cls, kind, label, room):
        # Проверяем, существует ли указанный тип устройства
        if kind not in cls.kinds:
            raise ValueError(f'Неизвестное устройство: {kind}')
        return cls.kinds[kind](label, room)


# Класс умного дома управляет устройствами и сценариями
class SmartHome:
    def __init__(self, address):
        self.address = address
        self._devices = {}  # Композиция: дом хранит созданные устройства
        self._owner, self._guard = Owner(), SecurityService()

    # Создаём устройство, подписываем наблюдателей и регистрируем его
    def add_device(self, kind, label, room):
        dev = DeviceFactory.create(kind, label, room)
        dev.subscribe(self._owner)
        dev.subscribe(self._guard)
        self._devices[label] = dev
        HomeController().register(dev)
        return dev

    # Сценарий меняет состояния нескольких устройств
    def scene(self, scene_name, commands):
        print(f'Сцена «{scene_name}»:')
        for label, state in commands.items():
            self._devices[label].set_state(state)


# Создаём умный дом и добавляем устройства
home = SmartHome('Бишкек, ул. Ибраимова 24')
home.add_device('lamp', 'Люстра', 'гостиная')
home.add_device('lamp', 'Торшер', 'спальня')
home.add_device('thermostat', 'Термостат', 'гостиная')
home.add_device('lock', 'Входной замок', 'прихожая')
home.add_device('camera', 'Камера двора', 'двор')

# Проверяем Singleton и количество устройств в общем реестре
print('Один контроллер?', HomeController() is HomeController(),
      '| устройств в реестре:', len(HomeController().registry))

# Запускаем сценарий «Вечер»
home.scene('Вечер', {'Люстра': 'вкл 40%', 'Термостат': '23°C'})

# Запускаем сценарий «Ночь»
home.scene('Ночь', {
    'Люстра': 'выкл',
    'Торшер': 'выкл',
    'Входной замок': 'закрыт',
    'Камера двора': 'запись'
})