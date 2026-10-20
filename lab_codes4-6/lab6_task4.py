# Лабораторная работа 6, задание 4. Система мониторинга


# Singleton: единый реестр всех датчиков
class SensorHub:
    _only = None

    def __new__(cls):
        # Создаём хаб только один раз
        if cls._only is None:
            cls._only = super().__new__(cls)
            cls._only.sensors = []  # Общий список датчиков
        return cls._only


# Наблюдатель: записывает и выводит предупреждения
class AlertService:
    def __init__(self):
        self.log = []  # История тревог

    def update(self, sensor, value):
        # Сохраняем информацию о превышении порога
        self.log.append(f'{sensor.kind} = {value} {sensor.unit} (порог {sensor.limit})')
        print(f'[Тревога] {sensor.place}: {sensor.kind} {value} {sensor.unit}!')


# Наблюдатель: отображает состояние датчиков и историю тревог
class Dashboard:
    def __init__(self, alerts):
        self.alerts = alerts
        self.tracked = []  # Агрегация: датчики передаются извне

    # Добавляем датчик на табло и подписываем наблюдателей
    def attach(self, sensor):
        self.tracked.append(sensor)
        sensor.subscribe(self)
        sensor.subscribe(self.alerts)

    # Получаем уведомление об изменении показаний
    def update(self, sensor, value):
        pass  # Последнее значение сохраняется самим датчиком

    # Выводим текущие показания и состояние датчиков
    def status_report(self):
        print('Состояние датчиков:')
        for s in self.tracked:
            # Проверяем, превышен ли допустимый порог
            flag = 'ВНИМАНИЕ' if s.last is not None and s.last > s.limit else 'норма'
            print(f'{s.place:<12}{s.kind:<12}{s.last} {s.unit:<5} {flag}')

    # Выводим историю всех тревог
    def alert_history(self):
        print('История тревог:', *self.alerts.log, sep='\n  ')


# Базовый класс датчика
class Sensor:
    kind, unit, limit = 'датчик', '', 0

    def __init__(self, place):
        self.place = place
        self.last = None  # Последнее измеренное значение
        self._watchers = []  # Список наблюдателей

    # Подписываем наблюдателя на показания датчика
    def subscribe(self, w):
        self._watchers.append(w)

    # Считываем значение и проверяем порог
    def read(self, value):
        self.last = value

        # Уведомляем наблюдателей только при превышении порога
        if value > self.limit:
            for w in self._watchers:
                w.update(self, value)


# Датчик температуры: порог 30 °C
class Temperature(Sensor):
    kind, unit, limit = 'температура', '°C', 30


# Датчик влажности: порог 70 %
class Humidity(Sensor):
    kind, unit, limit = 'влажность', '%', 70


# Датчик давления: порог 1030 гПа
class Pressure(Sensor):
    kind, unit, limit = 'давление', 'гПа', 1030


# Датчик углекислого газа: порог 1000 ppm
class CO2(Sensor):
    kind, unit, limit = 'CO2', 'ppm', 1000


# Датчик шума: порог 70 дБ
class Noise(Sensor):
    kind, unit, limit = 'шум', 'дБ', 70


# Factory: создаёт датчики нужного типа
class SensorFactory:
    kinds = {
        'temp': Temperature,
        'hum': Humidity,
        'press': Pressure,
        'co2': CO2,
        'noise': Noise
    }

    @classmethod
    def create(cls, kind, place):
        # Создаём датчик выбранного типа
        sensor = cls.kinds[kind](place)

        # Автоматически добавляем датчик в общий реестр
        SensorHub().sensors.append(sensor)
        return sensor


# Создаём табло и сервис тревог
board = Dashboard(AlertService())

# Создаём датчики и подключаем их к табло
for kind, place in [
    ('temp', 'Серверная'),
    ('co2', 'Аудитория 3'),
    ('noise', 'Коридор'),
    ('hum', 'Склад')
]:
    board.attach(SensorFactory.create(kind, place))

# Проверяем Singleton и количество зарегистрированных датчиков
print(
    'Датчиков в SensorHub:', len(SensorHub().sensors),
    '| хаб один:', SensorHub() is SensorHub()
)

# Передаём датчикам измеренные значения
readings = [(0, 27), (0, 34), (1, 1250), (2, 55), (3, 72), (1, 880)]

for index, val in readings:
    SensorHub().sensors[index].read(val)

# Выводим текущие показания всех датчиков
board.status_report()

# Выводим историю тревог
board.alert_history()