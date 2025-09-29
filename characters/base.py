from core.entities import Character
from core.mixins import CritMixin, SilenceMixin
from core.exceptions import NotEnoughMPError, SkillOnCooldownError, CharacterDeadError


class PartyCharacter(Character, CritMixin, SilenceMixin):
    """Базовый класс для персонажей пати"""

    def __init__(self, name, level=1):
        super().__init__(name, level)
        SilenceMixin.__init__(self)
        self._skill_cooldown = 0

    def basic_attack(self, target):
        """Базовая атака с возможностью крита"""
        if not self.is_alive:
            raise CharacterDeadError(f"{self.name} мертв и не может атаковать")

        if not target.is_alive:
            raise CharacterDeadError(f"Цель {target.name} мертва")

        base_damage = self.strength * 1.2
        damage, is_crit = self.calculate_crit(base_damage, 0.15, 1.8)

        target.take_damage(damage)

        message = f"{self.name} атакует {target.name}"
        if is_crit:
            message += f" КРИТИЧЕСКИЙ УРОН!"
        message += f" Нанесено урона: {damage:.1f}"

        return message

    def can_use_skill(self):
        """Проверка возможности использования навыка"""
        if self._skill_cooldown > 0:
            raise SkillOnCooldownError(f"Навык на перезарядке: {self._skill_cooldown} ходов")
        if self.is_silenced:
            raise SkillOnCooldownError(f"{self.name} немой и не может использовать навыки")
        return True

    def start_cooldown(self, rounds=3):
        """Запуск перезарядки навыка"""
        self._skill_cooldown = rounds

    def update_cooldown(self):
        """Обновление перезарядки"""
        if self._skill_cooldown > 0:
            self._skill_cooldown -= 1