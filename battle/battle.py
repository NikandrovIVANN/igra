import json
from core.mixins import LoggerMixin, SerializableMixin
from .turn_order import TurnOrder


class Boss(LoggerMixin, SerializableMixin):
    """Класс Босса"""

    def __init__(self, name, level=10):
        self.name = name
        self.level = level
        LoggerMixin.__init__(self)

        # Характеристики
        self.max_hp = 400
        self.hp = 400
        self.max_mp = 200
        self.mp = 200
        self.strength = 60
        self.agility = 30
        self.intelligence = 40
        self.effects = []

    @property
    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        """Нанесение урона боссу"""
        self.hp -= damage
        self.hp = max(0, self.hp)
        return self.hp <= 0

    def restore_hp(self, amount):
        """Восстановление HP"""
        self.hp = min(self.hp + amount, self.max_hp)

    def choose_action(self, targets):
        """Выбор действия для босса"""
        alive_targets = [t for t in targets if t.is_alive]
        if not alive_targets:
            return "Босс не видит целей для атаки"

        # Простая логика босса
        import random

        # Если HP мало - лечится
        if self.hp < self.max_hp * 0.3 and self.mp >= 20:
            self.mp -= 20
            heal_amount = self.intelligence * 1.5
            old_hp = self.hp
            self.restore_hp(heal_amount)
            actual_heal = self.hp - old_hp
            return f"Босс концентрируется и восстанавливает {actual_heal:.1f} HP"

        # Иначе атакует случайную цель
        target = random.choice(alive_targets)
        damage = self.strength * 1.8
        target.take_damage(damage)
        return f"Босс атакует {target.name}! Урон: {damage:.1f}"

    def update_effects(self):
        """Обновление эффектов"""
        for effect in self.effects[:]:
            effect.duration -= 1
            if effect.duration <= 0:
                self.effects.remove(effect)
                if hasattr(effect, 'remove'):
                    effect.remove(self)

    def add_effect(self, effect):
        """Добавление эффекта"""
        self.effects.append(effect)
        if hasattr(effect, 'apply'):
            effect.apply(self)

    def __str__(self):
        return f"👹 {self.name} - HP: {self.hp}/{self.max_hp}"


class Battle(LoggerMixin, SerializableMixin):
    """Класс управления боем"""

    def __init__(self, party, boss):
        LoggerMixin.__init__(self)
        self.party = party
        self.boss = boss
        self.turn_order = None
        self.round_number = 0
        self.is_battle_over = False
        self.winner = None

        # Инициализация порядка ходов
        self.update_turn_order()

    def update_turn_order(self):
        """Обновление порядка ходов"""
        all_participants = self.party + [self.boss]
        self.turn_order = TurnOrder(all_participants)

    def process_effects(self):
        """Обработка эффектов в начале раунда"""
        self.add_log(f"\n--- Раунд {self.round_number} ---")

        # Обработка эффектов для всех участников
        for participant in self.party + [self.boss]:
            if participant.is_alive:
                # Обновление эффектов
                participant.update_effects()

                # Обновление кулдаунов
                if hasattr(participant, 'update_cooldown'):
                    participant.update_cooldown()

                # Обновление немоты
                if hasattr(participant, 'update_silence'):
                    participant.update_silence()

    def check_battle_end(self):
        """Проверка условий окончания битвы"""
        party_alive = any(char.is_alive for char in self.party)
        boss_alive = self.boss.is_alive

        if not party_alive:
            self.is_battle_over = True
            self.winner = "boss"
            self.add_log("💀 Босс побеждает! Все персонажи мертвы.")
            return True

        if not boss_alive:
            self.is_battle_over = True
            self.winner = "party"
            self.add_log("🎉 Победа! Босс повержен!")
            return True

        return False

    def play_round(self):
        """Проведение одного раунда боя"""
        if self.is_battle_over:
            return

        self.round_number += 1
        self.process_effects()

        if self.check_battle_end():
            return

        # Ходы всех участников
        for participant in self.turn_order:
            if self.check_battle_end():
                break

            if not participant.is_alive:
                continue

            self.add_log(f"\nХод {participant.name}:")

            if participant == self.boss:
                # Ход босса
                action_result = self.boss.choose_action(self.party)
                self.add_log(action_result)
            else:
                # Ход персонажа
                self.player_turn(participant)

            # Проверяем конец боя после каждого хода
            if self.check_battle_end():
                break

    def player_turn(self, character):
        """Ход игрового персонажа"""
        alive_targets = [t for t in self.party + [self.boss] if t != character and t.is_alive]

        if not alive_targets:
            self.add_log(f"{character.name} не видит целей для атаки")
            return

        try:
            # 70% шанс использовать базовую атаку, 30% - навык
            import random
            if random.random() < 0.7 or character.mp < 20:
                # Базовая атака
                target = self.boss if self.boss.is_alive else alive_targets[0]
                result = character.basic_attack(target)
            else:
                # Использование навыка
                from characters.healer import Healer
                if isinstance(character, Healer):
                    # Лекарь лечит самого раненого союзника
                    wounded_allies = [p for p in self.party if p.is_alive and p.hp < p.max_hp * 0.8]
                    target = min(wounded_allies, key=lambda x: x.hp) if wounded_allies else character
                else:
                    # Остальные атакуют босса или случайную цель
                    target = self.boss if self.boss.is_alive else alive_targets[0]

                result = character.use_skill(target)

            self.add_log(result)

        except Exception as e:
            self.add_log(f"{character.name} не может действовать: {e}")

    def save_state(self, filename):
        """Сохранение состояния боя в файл"""
        state = {
            'round_number': self.round_number,
            'party': [char.to_dict() for char in self.party],
            'boss': self.boss.to_dict(),
            'winner': self.winner
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

        self.add_log(f"Состояние сохранено в {filename}")

    def display_status(self):
        """Отображение текущего статуса боя"""
        self.add_log("\n=== ТЕКУЩЕЕ СОСТОЯНИЕ ===")

        for char in self.party:
            status = "💀 МЕРТВ" if not char.is_alive else "❤️ ЖИВ"
            self.add_log(f"{char} | {status}")

        boss_status = "💀 МЕРТВ" if not self.boss.is_alive else "❤️ ЖИВ"
        self.add_log(f"{self.boss} | {boss_status}")