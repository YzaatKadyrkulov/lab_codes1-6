# Лабораторная работа 1, задание 3. Класс «Рецепт»
class Recipe:
    # конструктор: вызывается автоматически при создании объекта
    def __init__(self, dish, kitchen, minutes, level, portions):
        # атрибуты экземпляра: у каждого рецепта свои значения
        self.dish = dish                   # название блюда
        self.kitchen = kitchen             # кухня
        self.minutes = minutes             # время приготовления, мин
        self.level = level                 # сложность
        self.portions = portions           # количество порций

    # сравниваем время приготовления с заданным порогом limit
    def is_quick(self, limit):
        return self.minutes < limit

    # собираем описание из атрибутов конкретного объекта (self)
    def describe(self):
        return (f'{self.dish} | кухня: {self.kitchen} | {self.minutes} мин | '
                f'сложность: {self.level} | порций: {self.portions}')

    # время приготовления, приходящееся на одну порцию
    def per_person_time(self):
        if self.portions == 0:             # защита от деления на ноль
            return 0
        return round(self.minutes / self.portions, 1)


# создаём четыре объекта одного класса с разными данными
cookbook = [
    Recipe('Бешбармак', 'кыргызская', 150, 'сложный', 6),
    Recipe('Омлет', 'французская', 15, 'лёгкий', 2),
    Recipe('Лагман', 'уйгурская', 80, 'сложный', 4),
    Recipe('Пицца', 'итальянская', 35, 'средний', 3),
]

# вызываем методы у каждого объекта в цикле
for rec in cookbook:
    print(rec.describe())
    # порог 40 мин передаём в метод как аргумент
    print(f'быстрое (до 40 мин): {rec.is_quick(40)}; '
          f'время на порцию: {rec.per_person_time()} мин')