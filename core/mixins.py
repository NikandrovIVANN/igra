import json
from datetime import datetime


class CritMixin:
    """Миксин для критического урона"""

    def calculate_crit(self, base_damage, crit_chance=0.1, crit_multiplier=1.5):
        import random
        if random.random() < crit_chance:
            return base_damage * crit_multiplier, True
        return base_damage, False


class LoggerMixin:
    """Миксин для логирования действий"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = []

    def add_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.log.append(log_entry)
        print(log_entry)

    def get_log(self):
        return self.log.copy()


class SilenceMixin:
    """Миксин для эффекта немоты (блокировка навыков)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_silenced = False

    @property
    def is_silenced(self):
        return self._is_silenced

    def apply_silence(self, duration=2):
        self._is_silenced = True
        self._silence_duration = duration

    def update_silence(self):
        if self._is_silenced:
            self._silence_duration -= 1
            if self._silence_duration <= 0:
                self._is_silenced = False


class SerializableMixin:
    """Миксин для сериализации состояния"""

    def to_dict(self):
        """Преобразует объект в словарь для сериализации"""
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                result[key] = value
            elif hasattr(value, 'to_dict'):
                result[key[1:]] = value.to_dict()
            else:
                result[key[1:]] = value
        return result

    def to_json(self):
        """Сериализует объект в JSON"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)