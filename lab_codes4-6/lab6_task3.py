# Лабораторная работа 6, задание 3. Интернет-магазин


# Singleton + наблюдатель: единый сервис учёта товаров на складе
class InventoryService:
    _only = None

    def __new__(cls):
        # Создаём только один экземпляр сервиса
        if cls._only is None:
            cls._only = super().__new__(cls)
            cls._only.stock = {}  # Словарь товаров и их остатков
        return cls._only

    # Обрабатываем событие покупки и обновляем остатки
    def update(self, event, product, qty):
        if event == 'checkout':
            self.stock[product.name] -= qty
            print(f'   [Склад] «{product.name}»: списано {qty}, остаток {self.stock[product.name]}')


# Наблюдатель: отправляет уведомления о действиях с товарами
class NotificationService:
    def update(self, event, product, qty):
        print(f'   [Уведомление] {event}: {product.name} × {qty}')


# Класс товара: товар существует независимо от корзины (агрегация)
class Product:
    def __init__(self, name, price, amount):
        self.name, self.price = name, price
        InventoryService().stock[name] = amount  # Записываем количество на складе


# Одна позиция в корзине: товар и его количество
class CartItem:
    def __init__(self, product, qty):
        self.product, self.qty = product, qty

    # Рассчитываем стоимость позиции
    def total(self):
        return self.product.price * self.qty


# Корзина покупателя
class ShoppingCart:
    def __init__(self):
        self._lines = []  # Композиция: позиции создаются внутри корзины
        # Подписываем сервисы на события корзины
        self._watchers = [NotificationService(), InventoryService()]

    # Отправляем событие всем наблюдателям
    def _notify(self, event, product, qty):
        for w in self._watchers:
            w.update(event, product, qty)

    # Добавляем товар в корзину и уведомляем сервисы
    def add(self, product, qty):
        self._lines.append(CartItem(product, qty))
        self._notify('добавлено в корзину', product, qty)

    # Оформляем заказ, рассчитываем скидку и принимаем оплату
    def checkout(self, payment):
        subtotal = sum(l.total() for l in self._lines)  # Общая стоимость товаров

        # Определяем скидку в зависимости от суммы заказа
        discount = 0.10 if subtotal > 20000 else 0.05 if subtotal > 8000 else 0
        total = subtotal * (1 - discount)

        print(f'Сумма: {subtotal} сом, скидка {discount:.0%}, к оплате: {total:.2f} сом')

        # Выполняем оплату выбранным способом
        print(payment.pay(total))

        # Уведомляем сервисы о покупке и списываем товары со склада
        for l in self._lines:
            self._notify('checkout', l.product, l.qty)


# Способ оплаты банковской картой
class CardPayment:
    def pay(self, s): return f'Оплата картой: {s:.2f} сом'


# Способ оплаты наличными
class CashPayment:
    def pay(self, s): return f'Оплата наличными: {s:.2f} сом'


# Способ оплаты по QR-коду
class QRPayment:
    def pay(self, s): return f'Оплата по QR-коду: {s:.2f} сом'


# Оплата в рассрочку на 6 месяцев
class InstallmentPayment:
    def pay(self, s): return f'Рассрочка на 6 мес.: {s / 6:.2f} сом в месяц'


# Factory: создаёт объект выбранного способа оплаты
class PaymentFactory:
    kinds = {
        'card': CardPayment,
        'cash': CashPayment,
        'qr': QRPayment,
        'installment': InstallmentPayment
    }

    @classmethod
    def create(cls, kind):
        return cls.kinds[kind]()


# Создаём товары и указываем их начальные остатки на складе
laptop = Product('Ноутбук', 38000, 5)
mouse = Product('Мышь', 750, 40)
bag = Product('Рюкзак', 2400, 12)

# Создаём корзину и добавляем товары
cart = ShoppingCart()
cart.add(laptop, 1)
cart.add(mouse, 2)
cart.add(bag, 1)

# Проверяем, что сервис склада существует в единственном экземпляре
print('Склад один:', InventoryService() is InventoryService())

# Оформляем заказ с оплатой в рассрочку
cart.checkout(PaymentFactory.create('installment'))