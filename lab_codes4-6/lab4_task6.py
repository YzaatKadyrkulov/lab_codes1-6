# Лабораторная работа 4, задание 6. Персонажи ролевой игры
from abc import ABC, abstractmethod


# Абстрактный базовый класс для всех игровых персонажей
class GameCharacter(ABC):
    def __init__(self, nick, hp):
        self.nick, self.hp, self.lvl = nick, hp, 1  # Ник, здоровье и начальный уровень

    # Каждый персонаж должен реализовать атаку, защиту и повышение уровня
    @abstractmethod
    def attack(self): ...

    @abstractmethod
    def defend(self): ...

    @abstractmethod
    def level_up(self): ...

    # Получаем урон от врага с учётом защиты
    def take_hit(self, enemy):
        dmg = max(1, enemy.attack() - self.defend())  # Минимальный урон — 1
        self.hp = max(0, self.hp - dmg)  # Здоровье не может быть меньше 0
        print(f'  {enemy.nick} → {self.nick}: урон {dmg}, осталось HP {self.hp}')


# Класс воина
class Warrior(GameCharacter):
    def __init__(self, nick, hp, strength, armor, weapon):
        super().__init__(nick, hp)
        self.strength, self.armor, self.weapon = strength, armor, weapon

    # Сила атаки зависит от силы персонажа и уровня
    def attack(self): return self.strength * 2 + self.lvl

    # Броня определяет защиту воина
    def defend(self): return self.armor

    # Повышаем уровень и увеличиваем силу
    def level_up(self): self.lvl += 1; self.strength += 3


# Класс мага
class Mage(GameCharacter):
    def __init__(self, nick, hp, magic, mana, school):
        super().__init__(nick, hp)
        self.magic, self.mana, self.school = magic, mana, school

    # При достаточном количестве маны маг наносит усиленный урон
    def attack(self): return self.magic * 3 if self.mana >= 10 else 4

    # Защита мага равна 3
    def defend(self): return 3

    # Повышаем уровень, магию и запас маны
    def level_up(self): self.lvl += 1; self.magic += 4; self.mana += 15


# Класс лучника
class Archer(GameCharacter):
    def __init__(self, nick, hp, aim, arrows, bow):
        super().__init__(nick, hp)
        self.aim, self.arrows, self.bow = aim, arrows, bow

    # Для атаки нужны стрелы; каждая атака расходует одну стрелу
    def attack(self):
        if self.arrows == 0:
            return 2  # Если стрел нет, наносится слабый урон
        self.arrows -= 1
        return self.aim * 2 + 6

    def defend(self): return 5

    # Повышаем уровень, меткость и запас стрел
    def level_up(self): self.lvl += 1; self.aim += 3; self.arrows += 10


# Класс целителя
class Healer(GameCharacter):
    def __init__(self, nick, hp, heal, mana, guard):
        super().__init__(nick, hp)
        self.heal, self.mana, self.guard = heal, mana, guard

    # Сила атаки целителя зависит от параметра лечения
    def attack(self): return self.heal // 2

    def defend(self): return self.guard

    # Повышаем уровень, силу лечения и защиту
    def level_up(self): self.lvl += 1; self.heal += 3; self.guard += 2


# Создаём список персонажей разных классов
heroes = [
    Warrior('Манас', 120, 14, 8, 'меч'),
    Mage('Алтын', 80, 12, 60, 'огонь'),
    Archer('Эрмек', 90, 13, 20, 'длинный'),
    Healer('Айсулуу', 85, 10, 50, 6),
]

# Первые два персонажа повышают свой уровень
for h in heroes[:2]:
    h.level_up()

# Организуем турнир: каждый персонаж атакует следующего
print('Турнир: каждый атакует следующего')
for i, hero in enumerate(heroes):
    target = heroes[(i + 1) % len(heroes)]  # Последний атакует первого
    target.take_hit(hero)

# Определяем победителя по оставшемуся количеству здоровья
winner = max(heroes, key=lambda h: h.hp)
print('Победитель по остатку HP:', winner.nick, winner.hp)