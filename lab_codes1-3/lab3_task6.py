# Лабораторная работа 3, задание 6. Продукты питания
# родительский класс: общие данные и методы для любого продукта
class Food:
    def __init__(self, product, kcal, prot, fat, carb, kg_price):
        self.product = product
        self.kcal = kcal                   # ккал на 100 г
        # белки, жиры, углеводы на 100 г (присваивание сразу трёх атрибутов)
        self.prot, self.fat, self.carb = prot, fat, carb
        self.kg_price = kg_price           # цена за кг

    # этикетка с БЖУ
    def label(self):
        return (f'{self.product}: {self.kcal} ккал | Б {self.prot} / '
                f'Ж {self.fat} / У {self.carb} (на 100 г)')

    # калорийность порции пропорциональна её массе
    def calories_per_serving(self, serving_g):
        return round(self.kcal * serving_g / 100)


# наследование: молочный продукт получает все методы Food и дополняет их
class Dairy(Food):
    def __init__(self, product, kcal, prot, fat, carb, kg_price, fat_pct, shelf_days, kind):
        # вызываем конструктор родителя для общих атрибутов
        super().__init__(product, kcal, prot, fat, carb, kg_price)
        # атрибуты, которые есть только у молочных продуктов
        self.fat_pct, self.shelf_days, self.kind = fat_pct, shelf_days, kind

    # переопределение: расширяем этикетку родителя через super(), а не копируем её
    def label(self):
        return f'{super().label()} | {self.kind}, жирность {self.fat_pct}%'

    # продукт свежий, если срок годности не превышен
    def is_fresh(self, days):
        return days <= self.shelf_days


class Bakery(Food):
    def __init__(self, product, kcal, prot, fat, carb, kg_price, content, weight_g, kind):
        super().__init__(product, kcal, prot, fat, carb, kg_price)
        # состав, масса изделия и его тип
        self.content, self.weight_g, self.kind = content, weight_g, kind

    def label(self):
        return f'{super().label()} | {self.kind}, {self.weight_g} г, состав: {self.content}'


# два молочных продукта и два хлебобулочных в одном списке
goods = [
    Dairy('Кефир', 51, 3.0, 2.5, 4.0, 90, 2.5, 7, 'кефир'),
    Dairy('Сыр сулугуни', 290, 20.0, 22.0, 0.5, 620, 45, 30, 'сыр'),
    Bakery('Лепёшка', 265, 8.0, 1.5, 54.0, 110, 'мука, вода, соль', 300, 'хлеб'),
    Bakery('Медовик', 400, 5.5, 18.0, 55.0, 780, 'мука, мёд, сметана', 800, 'торт'),
]
for g in goods:
    print(g.label())                       # вызывается версия label() нужного класса
    print(f'порция 150 г: {g.calories_per_serving(150)} ккал')
    # is_fresh() есть только у молочных продуктов, поэтому сначала проверяем тип
    if isinstance(g, Dairy):
        print(f'   свежий на 10-й день: {g.is_fresh(10)}')