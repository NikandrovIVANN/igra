class Effect:
    """Базовый класс эффекта"""

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def apply(self, target):
        """Применить эффект к цели"""
        pass

    def remove(self, target):
        """Удалить эффект с цели"""
        pass

    def process_turn(self, target):
        """Обработать эффект в начале хода"""
        pass

    def __str__(self):
        return f"{self.name} ({self.duration} ходов)"


class BurnEffect(Effect):
    """Эффект горения - урон каждый ход"""

    def __init__(self, duration=3, damage_per_turn=10):
        super().__init__("Горение", duration)
        self.damage_per_turn = damage_per_turn

    def apply(self, target):
        if hasattr(target, 'add_log'):
            target.add_log(f"{target.name} начинает гореть!")

    def remove(self, target):
        if hasattr(target, 'add_log'):
            target.add_log(f"{target.name} перестал гореть")

    def process_turn(self, target):
        if target.is_alive:
            target.take_damage(self.damage_per_turn)
            if hasattr(target, 'add_log'):
                target.add_log(f"{target.name} получает {self.damage_per_turn} урона от горения")


class RegenerationEffect(Effect):
    """Эффект регенерации - лечение каждый ход"""

    def __init__(self, duration=2, heal_per_turn=5):
        super().__init__("Регенерация", duration)
        self.heal_per_turn = heal_per_turn

    def apply(self, target):
        if hasattr(target, 'add_log'):
            target.add_log(f"{target.name} начинает регенерировать")

    def remove(self, target):
        if hasattr(target, 'add_log'):
            target.add_log(f"{target.name} перестал регенерировать")

    def process_turn(self, target):
        if target.is_alive:
            old_hp = target.hp
            target.restore_hp(self.heal_per_turn)
            actual_heal = target.hp - old_hp
            if actual_heal > 0 and hasattr(target, 'add_log'):
                target.add_log(f"{target.name} восстанавливает {actual_heal} HP от регенерации")