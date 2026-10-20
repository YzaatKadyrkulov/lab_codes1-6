# Лабораторная работа 6, задание 5. Ресторан


# Singleton: единый реестр всех заказов ресторана
class Kitchen:
    _only = None

    def __new__(cls):
        # Создаём только один экземпляр кухни
        if cls._only is None:
            cls._only = super().__new__(cls)
            cls._only.orders = []  # Общий список заказов
        return cls._only


# Блюдо из меню — агрегация
class Dish:
    def __init__(self, title, category, price, minutes):
        self.title = title
        self.category = category
        self.price = price
        self.minutes = minutes


# Factory: создаёт блюда с ценой и временем приготовления
class MenuFactory:
    BASE = {
        'салат': (180, 8),
        'суп': (220, 15),
        'горячее': (420, 30),
        'десерт': (190, 10)
    }

    @classmethod
    def create(cls, title, category, extra=0):
        # Получаем базовую цену и время по категории
        price, minutes = cls.BASE[category]

        # Создаём блюдо с учётом дополнительной стоимости
        return Dish(title, category, price + extra, minutes)


# Наблюдатель: повар получает уведомления об изменении статуса
class Chef:
    def update(self, order, status):
        print(f'[Повар] заказ №{order.number}: {status}')


# Наблюдатель: официант получает уведомления о заказах
class Waiter:
    def update(self, order, status):
        print(f'[Официант] стол {order.table}, заказ №{order.number}: {status}')


# Одна позиция заказа: блюдо и его количество
class OrderItem:
    def __init__(self, dish, qty):
        self.dish = dish
        self.qty = qty


# Заказ посетителя
class Order:
    counter = 0  # Счётчик номеров заказов

    STATUSES = ['принят', 'готовится', 'готов', 'выдан', 'отменён']

    def __init__(self, table):
        Order.counter += 1

        # Присваиваем заказу номер, стол и начальный статус
        self.number = Order.counter
        self.table = table
        self.status = 'принят'

        self._lines = []  # Композиция: позиции создаются внутри заказа
        self._watchers = [Chef(), Waiter()]  # Подписываем наблюдателей

        # Регистрируем заказ в общей кухне
        Kitchen().orders.append(self)

    # Добавляем блюдо в заказ
    def add(self, dish, qty=1):
        self._lines.append(OrderItem(dish, qty))

    # Меняем статус заказа и уведомляем повара с официантом
    def set_status(self, new):
        if new not in self.STATUSES:
            raise ValueError(f'Неизвестный статус: {new}')

        self.status = new

        # Отправляем уведомление каждому наблюдателю
        for w in self._watchers:
            w.update(self, new)

    # Рассчитываем общую стоимость заказа
    def bill(self):
        return sum(l.dish.price * l.qty for l in self._lines)

    # Определяем время приготовления по самому долгому блюду
    def cook_time(self):
        return max(l.dish.minutes for l in self._lines)


# Создаём меню ресторана через фабрику
menu = [
    MenuFactory.create('Ачык-чучук', 'салат'),
    MenuFactory.create('Лагман', 'суп', 30),
    MenuFactory.create('Плов', 'горячее', 40),
    MenuFactory.create('Чак-чак', 'десерт')
]

# Создаём первый заказ и добавляем блюда
o1 = Order(table=4)
o1.add(menu[0])
o1.add(menu[1], 2)
o1.add(menu[3])

# Создаём второй заказ
o2 = Order(table=7)
o2.add(menu[2], 3)
o2.add(menu[0], 2)

# Создаём третий заказ
o3 = Order(table=2)
o3.add(menu[1])

# Проверяем Singleton и количество заказов
print('Кухня одна:', Kitchen() is Kitchen(), '| заказов:', len(Kitchen().orders))

# Меняем статусы заказов — повар и официант получают уведомления
o1.set_status('готовится')
o1.set_status('готов')
o1.set_status('выдан')

o2.set_status('готовится')
o3.set_status('отменён')

# Исключаем отменённые заказы из расчётов
done = [o for o in Kitchen().orders if o.status != 'отменён']

# Рассчитываем среднее время приготовления
print(
    f'Среднее время приготовления: '
    f'{sum(o.cook_time() for o in done) / len(done):.1f} мин'
)

# Рассчитываем средний чек
print(
    f'Средний чек: '
    f'{sum(o.bill() for o in done) / len(done):.1f} сом'
)