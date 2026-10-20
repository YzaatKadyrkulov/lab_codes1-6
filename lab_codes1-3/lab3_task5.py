# Лабораторная работа 3, задание 5. Недвижимость
# родительский класс: общие данные и методы для любого объекта недвижимости
class Property:
    def __init__(self, place, square, price, built):
        self.place = place                 # адрес
        self.square = square               # площадь, кв. м
        self.price = price                 # цена, $
        self.built = built                 # год постройки

    # стоимость одного квадратного метра, округлённая до целого
    def price_per_sqm(self):
        return round(self.price / self.square)

    # укладывается ли цена объекта в бюджет
    def is_affordable(self, budget):
        return self.price <= budget

    # возраст здания: текущий год минус год постройки
    def age(self):
        return 2026 - self.built

    def describe(self):
        return f'{self.place}, {self.square} м², ${self.price}, возраст {self.age()}'


# наследование: квартира получает все методы Property и дополняет их
class Apartment(Property):
    def __init__(self, place, square, price, built, floor, rooms, balcony, market):
        # вызываем конструктор родителя для общих атрибутов
        super().__init__(place, square, price, built)
        # атрибуты, которые есть только у квартиры
        self.floor, self.rooms, self.balcony, self.market = floor, rooms, balcony, market

    # переопределение: расширяем описание родителя через super(), а не копируем его
    def describe(self):
        bal = 'с балконом' if self.balcony else 'без балкона'
        return (f'Квартира: {super().describe()}; {self.floor} этаж, '
                f'{self.rooms}-комн., {bal}, {self.market}')


class House(Property):
    def __init__(self, place, square, price, built, storeys, plot, material, garage):
        super().__init__(place, square, price, built)
        # атрибуты дома: этажность, участок (сотки), материал, наличие гаража
        self.storeys, self.plot, self.material, self.garage = storeys, plot, material, garage

    def describe(self):
        gar = 'есть гараж' if self.garage else 'нет гаража'
        return (f'Дом: {super().describe()}; {self.storeys} эт., участок {self.plot} сот., '
                f'{self.material}, {gar}')


# рынок: две квартиры и два дома в одном списке
market = [
    Apartment('Бишкек, мкр Асанбай', 62, 78000, 2022, 7, 2, True, 'новостройка'),
    Apartment('Бишкек, ул. Токтогула', 48, 52000, 1985, 3, 2, False, 'вторичка'),
    House('Ош, Нариман', 140, 95000, 2015, 2, 6, 'кирпич', True),
    House('Каракол, центр', 90, 61000, 2008, 1, 5, 'газобетон', False),
]

# методы price_per_sqm() и is_affordable() определены один раз в родителе
# и работают одинаково для квартир и домов
for obj in market:
    print(obj.describe())
    print(f'цена за м²: ${obj.price_per_sqm()}; до $70 000: {obj.is_affordable(70000)}')

# лучшее соотношение цена/площадь — минимальная цена за м²
best = min(market, key=lambda o: o.price_per_sqm())
print('Лучшее соотношение цена/площадь:', best.place, f'(${best.price_per_sqm()}/м²)')