class BoundedStat:
    """Дескриптор для валидации характеристик в заданных пределах"""

    def __init__(self, min_val=0, max_val=100):
        self.min_val = min_val
        self.max_val = max_val

    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, instance, owner):
        return getattr(instance, self.name, 0)

    def __set__(self, instance, value):
        value = max(self.min_val, min(value, self.max_val))
        setattr(instance, self.name, value)


class CooldownDescriptor:
    """Дескриптор для управления кулдаунами навыков"""

    def __init__(self, cooldown_rounds=3):
        self.cooldown_rounds = cooldown_rounds

    def __set_name__(self, owner, name):
        self.name = name
        self.cooldown_name = f"_{name}_cooldown"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.cooldown_name, 0) <= 0

    def __set__(self, instance, value):
        if value:  # Если навык используется
            setattr(instance, self.cooldown_name, self.cooldown_rounds)
