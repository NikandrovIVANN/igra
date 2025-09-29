from abc import ABC, abstractmethod
from battle.effects import ShieldEffect, RegenerationEffect


class Item(ABC):
    """Абстрактный класс предмета"""

    def __init__(self, name, description, consumable=True):
        self.name = name
        self.description = description
        self.consumable = consumable

    @abstractmethod
    def use(self, target):
        """Использовать предмет"""
        pass

    def __str__(self):
        return f"{self.name}: {self.description}"


class HealthPotion(Item):
    """Зелье здоровья"""

    def __init__(self):
        super().__init__("Зелье здоровья", "Восстанавливает 50 HP")

    def use(self, target):
        if target.is_alive:
            old_hp = target.hp
            target.restore_hp(50)
            actual_heal = target.hp - old_hp
            return f"{target.name} использует {self.name} и восстанавливает {actual_heal} HP"
        return f"{target.name} мертв и не может использовать предметы"


class ManaPotion(Item):
    """Зелье маны"""

    def __init__(self):
        super().__init__("Зелье маны", "Восстанавливает 30 MP")

    def use(self, target):
        if target.is_alive:
            old_mp = target.mp
            target.restore_mp(30)
            actual_restore = target.mp - old_mp
            return f"{target.name} использует {self.name} и восстанавливает {actual_restore} MP"
        return f"{target.name} мертв и не может использовать предметы"


class ShieldScroll(Item):
    """Свиток щита"""

    def __init__(self):
        super().__init__("Свиток щита", "Накладывает щит на 2 хода", consumable=True)

    def use(self, target):
        if target.is_alive:
            shield_effect = ShieldEffect(duration=2, shield_amount=40)
            target.add_effect(shield_effect)
            return f"{target.name} использует {self.name} и получает щит"
        return f"{target.name} мертв и не может использовать предметы"


class RegenerationPotion(Item):
    """Зелье регенерации"""

    def __init__(self):
        super().__init__("Зелье регенерации", "Постепенное восстановление HP", consumable=True)

    def use(self, target):
        if target.is_alive:
            regen_effect = RegenerationEffect(duration=3, heal_per_turn=15)
            target.add_effect(regen_effect)
            return f"{target.name} использует {self.name} и начинает регенерировать"
        return f"{target.name} мертв и не может использовать предметы"
