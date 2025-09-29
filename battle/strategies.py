from abc import ABC, abstractmethod
from core.mixins import LoggerMixin


class BossStrategy(ABC, LoggerMixin):
    """Абстрактная стратегия поведения босса"""

    def __init__(self, boss):
        super().__init__()
        self.boss = boss

    @abstractmethod
    def choose_action(self, targets):
        """Выбрать действие для босса"""
        pass


class AggressiveStrategy(BossStrategy):
    """Агрессивная стратегия - фокусируется на одном цели"""

    def choose_action(self, targets):
        alive_targets = [t for t in targets if t.is_alive]
        if not alive_targets:
            return "Босс не видит целей для атаки"

        # Выбираем цель с наименьшим HP
        target = min(alive_targets, key=lambda x: x.hp)

        if self.boss.mp >= 30 and len(alive_targets) > 1:
            # Используем AoE атаку если есть мана и несколько целей
            self.boss.mp -= 30
            message = f"Босс использует УДАР ВОЛНОЙ по всем целям!"
            for t in alive_targets:
                damage = self.boss.strength * 1.5
                t.take_damage(damage)
                message += f"\n  {t.name} получает {damage:.1f} урона"
            return message
        else:
            # Обычная атака
            damage = self.boss.strength * 2.0
            target.take_damage(damage)
            return f"Босс яростно атакует {target.name}! Урон: {damage:.1f}"


class DefensiveStrategy(BossStrategy):
    """Защитная стратегия - самолечение и щиты"""

    def choose_action(self, targets):
        # Если HP низкое - лечимся
        if self.boss.hp < self.boss.max_hp * 0.3 and self.boss.mp >= 20:
            self.boss.mp -= 20
            heal_amount = self.boss.intelligence * 1.5
            old_hp = self.boss.hp
            self.boss.restore_hp(heal_amount)
            actual_heal = self.boss.hp - old_hp
            return f"Босс концентрируется и восстанавливает {actual_heal:.1f} HP"

        # Иначе атакуем случайную цель
        alive_targets = [t for t in targets if t.is_alive]
        if alive_targets:
            import random
            target = random.choice(alive_targets)
            damage = self.boss.strength * 1.8
            target.take_damage(damage)
            return f"Босс атакует {target.name}! Урон: {damage:.1f}"

        return "Босс готовится к следующей атаке"


class MixedStrategy(BossStrategy):
    """Смешанная стратегия - баланс атаки и защиты"""

    def choose_action(self, targets):
        alive_targets = [t for t in targets if t.is_alive]

        # Если остался один персонаж - мощная атака
        if len(alive_targets) == 1 and self.boss.mp >= 25:
            self.boss.mp -= 25
            target = alive_targets[0]
            damage = self.boss.strength * 2.5
            target.take_damage(damage)
            return f"Босс использует ФИНАЛЬНЫЙ УДАР по {target.name}! Урон: {damage:.1f}"

        # Иначе случайный выбор между атакой и лечением
        import random
        if random.random() < 0.7 or not alive_targets:  # 70% шанс атаки
            if alive_targets:
                target = random.choice(alive_targets)
                damage = self.boss.strength * 1.6
                target.take_damage(damage)
                return f"Босс атакует {target.name}! Урон: {damage:.1f}"
        else:
            # Лечение
            if self.boss.mp >= 15:
                self.boss.mp -= 15
                heal_amount = self.boss.intelligence * 1.2
                old_hp = self.boss.hp
                self.boss.restore_hp(heal_amount)
                actual_heal = self.boss.hp - old_hp
                return f"Босс восстанавливает {actual_heal:.1f} HP"

        return "Босс наблюдает за битвой"
