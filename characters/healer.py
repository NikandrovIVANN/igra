from .base import PartyCharacter
from core.exceptions import NotEnoughMPError


class Healer(PartyCharacter):
    """Класс Лекаря - специалист по лечению и поддержке"""

    def __init__(self, name, level=1):
        super().__init__(name, level)
        self.strength = 25
        self.agility = 35
        self.intelligence = 75
        self.max_hp = 90
        self.hp = 90
        self.max_mp = 120
        self.mp = 120

    def use_skill(self, target):
        """Исцеление - восстанавливает HP цели"""
        self.can_use_skill()

        if self.mp < 20:
            raise NotEnoughMPError("Недостаточно MP для Исцеления")

        self.mp -= 20
        self.start_cooldown(2)

        heal_amount = self.intelligence * 1.8
        old_hp = target.hp
        target.restore_hp(heal_amount)
        actual_heal = target.hp - old_hp

        # Импортируем здесь чтобы избежать циклических импортов
        from battle.effects import RegenerationEffect

        # Накладываем эффект регенерации
        regen_effect = RegenerationEffect(duration=2, heal_per_turn=5)
        target.add_effect(regen_effect)

        message = f"{self.name} ИСЦЕЛЯЕТ {target.name} на {actual_heal:.1f} HP + регенерация"

        return message

    def __str__(self):
        return f"💚 {super().__str__()}"