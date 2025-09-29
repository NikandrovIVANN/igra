class GameException(Exception):
    """Базовое исключение для игровых ошибок"""
    pass

class NotEnoughMPError(GameException):
    """Недостаточно маны для использования навыка"""
    pass

class SkillOnCooldownError(GameException):
    """Навык на перезарядке"""
    pass

class CharacterDeadError(GameException):
    """Персонаж мертв"""
    pass