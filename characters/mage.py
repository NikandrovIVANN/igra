from .base import PartyCharacter
from core.exceptions import NotEnoughMPError


class Mage(PartyCharacter):
    """Класс Мага - специалист по магическому урону и эффектам"""

    def __init__(self, name, level=1):
        super().__init__(name, level)
        self.strength = 20
        self.agility = 30
        self.intelligence = 85
        self.max_hp = 80
        self.hp = 80
        self.max_mp = 100
        self.mp = 100

    def use_skill(self, target):
        """Огненный шар - наносит урон и накладывает эффект горения"""
        self.can_use_skill()

        if self.mp < 25:
            raise NotEnoughMPError("Недостаточно MP для Огненного шара")

        self.mp -= 25
        self.start_cooldown(3)

        base_damage = self.intelligence * 2.0
        damage, is_crit = self.calculate_crit(base_damage, 0.25, 2.2)

        target.take_damage(damage)

        # Импортируем здесь чтобы избежать циклических импортов
        from battle.effects import BurnEffect

        # Накладываем эффект горения
        burn_effect = BurnEffect(duration=3, damage_per_turn=10)
        target.add_effect(burn_effect)

        message = f"{self.name} бросает ОГНЕННЫЙ ШАР в {target.name}"
        if is_crit:
            message += f" КРИТИЧЕСКИЙ УРОН!"
        message += f" Нанесено урона: {damage:.1f} + эффект горения"

        return message

    def __str__(self):
        return f"🔮 {super().__str__()}"