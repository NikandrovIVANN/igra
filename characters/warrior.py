from .base import PartyCharacter
from core.exceptions import NotEnoughMPError


class Warrior(PartyCharacter):
    """Класс Воина - специалист по физическому урону"""

    def __init__(self, name, level=1):
        super().__init__(name, level)
        self.strength = 80
        self.agility = 40
        self.intelligence = 20
        self.max_hp = 150
        self.hp = 150
        self.max_mp = 30
        self.mp = 30

    def use_skill(self, target):
        """Мощная атака - наносит большой урон но тратит много MP"""
        self.can_use_skill()

        if self.mp < 15:
            raise NotEnoughMPError("Недостаточно MP для Мощной атаки")

        self.mp -= 15
        self.start_cooldown(2)

        base_damage = self.strength * 2.5
        damage, is_crit = self.calculate_crit(base_damage, 0.2, 2.0)

        target.take_damage(damage)

        message = f"{self.name} использует МОЩНУЮ АТАКУ на {target.name}"
        if is_crit:
            message += f" КРИТИЧЕСКИЙ УРОН!"
        message += f" Нанесено урона: {damage:.1f}"

        return message

    def __str__(self):
        return f"⚔️ {super().__str__()}"