from abc import ABC, abstractmethod
from .descriptions import BoundedStat
from .mixins import SerializableMixin


class Human(SerializableMixin):
    """Базовый класс для всех существ в игре"""
    hp = BoundedStat(0, 1000)
    mp = BoundedStat(0, 500)
    strength = BoundedStat(1, 100)
    agility = BoundedStat(1, 100)
    intelligence = BoundedStat(1, 100)

    def __init__(self, name, level=1):
        self.name = name
        self.level = level
        self._hp = 100
        self._mp = 50
        self._strength = 10
        self._agility = 10
        self._intelligence = 10
        self.max_hp = 100
        self.max_mp = 50
        self.effects = []

    def __str__(self):
        return f"{self.name} (Ур. {self.level}) - HP: {self.hp}/{self.max_hp}"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', level={self.level})"

    @property
    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        """Нанесение урона с проверкой на смерть"""
        self.hp -= damage
        return self.hp <= 0

    def restore_hp(self, amount):
        """Восстановление HP"""
        self.hp = min(self.hp + amount, self.max_hp)

    def restore_mp(self, amount):
        """Восстановление MP"""
        self.mp = min(self.mp + amount, self.max_mp)

    def update_effects(self):
        """Обновление длительности эффектов"""
        for effect in self.effects[:]:
            effect.duration -= 1
            if effect.duration <= 0:
                self.effects.remove(effect)
                if hasattr(effect, 'remove'):
                    effect.remove(self)

    def add_effect(self, effect):
        """Добавление эффекта к персонажу"""
        self.effects.append(effect)
        if hasattr(effect, 'apply'):
            effect.apply(self)


class Character(Human, ABC):
    """Абстрактный класс персонажа"""

    def __init__(self, name, level=1):
        super().__init__(name, level)
        self.skills_used = 0

    @abstractmethod
    def basic_attack(self, target):
        """Базовая атака - должна быть реализована в подклассах"""
        pass

    @abstractmethod
    def use_skill(self, target):
        """Использование навыка - должна быть реализована в подклассах"""
        pass