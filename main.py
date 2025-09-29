#!/usr/bin/env python3
"""
Главный файл игры "Пати против Босса"
"""

import random
import sys
import os

# Явно добавляем текущую директорию в путь импорта
sys.path.insert(0, os.path.dirname(__file__))

from characters import Warrior, Mage, Healer
from battle.battle import Battle, Boss  # Явно указываем подмодуль


def create_party():
    """Создание пати персонажей"""
    print("🎮 Создание пати персонажей!")

    party = []
    classes = {
        '1': ('Воин', Warrior),
        '2': ('Маг', Mage),
        '3': ('Лекарь', Healer)
    }

    print("\nДоступные классы:")
    print("1. ⚔️ Воин - сильная атака, много HP")
    print("2. 🔮 Маг - магический урон, эффекты")
    print("3. 💚 Лекарь - лечение, поддержка")

    for i in range(3):
        while True:
            choice = input(f"\nВыберите класс для персонажа {i + 1} (1-3): ").strip()
            if choice in classes:
                class_name, class_obj = classes[choice]
                name = input(f"Введите имя для {class_name}: ").strip()
                if not name:
                    name = f"{class_name}{i + 1}"

                character = class_obj(name)
                party.append(character)
                print(f"✅ Создан {class_name}: {name}")
                break
            else:
                print("❌ Неверный выбор. Попробуйте снова.")

    return party


def setup_boss():
    """Создание и настройка босса"""
    boss = Boss("Драконий Повелитель", level=15)
    return boss


def main():
    """Главная функция игры"""
    print("🐉 Добро пожаловать в игру 'Пати против Босса'! 🐉")
    print("=" * 50)

    # Настройка случайного генератора
    seed = input("Введите seed для генератора случайных чисел (или Enter для случайного): ").strip()
    if seed:
        try:
            random.seed(int(seed))
            print(f"✅ Установлен seed: {seed}")
        except ValueError:
            random.seed()
            print("❌ Неверный seed, используется случайный")
    else:
        random.seed()
        print("✅ Используется случайный seed")

    # Создание пати и босса
    party = create_party()
    boss = setup_boss()

    print("\n" + "=" * 50)
    print("🎯 Ваша пати готова к бою!")
    for char in party:
        print(f"  {char}")

    print(f"\n🐉 Ваш противник: {boss}")
    print("=" * 50)

    input("\nНажмите Enter чтобы начать бой...")

    # Создание и запуск боя
    battle = Battle(party, boss)

    # Игровой цикл
    while not battle.is_battle_over:
        battle.play_round()

        # Показываем статус после каждого раунда
        battle.display_status()

        if not battle.is_battle_over:
            input("\nНажмите Enter для продолжения...")

    # Конец игры
    print("\n" + "=" * 50)
    print("🎊 ИГРА ОКОНЧЕНA!")

    if battle.winner == "party":
        print("🎉 ПОБЕДА! Вы победили босса!")
    else:
        print("💀 ПОРАЖЕНИЕ! Босс победил вашу пати.")

    # Сохраняем лог боя
    log_filename = "battle_log.txt"
    with open(log_filename, 'w', encoding='utf-8') as f:
        for log_entry in battle.get_log():
            f.write(log_entry + '\n')

    print(f"\n📝 Лог боя сохранен в файл: {log_filename}")

    # Сохраняем состояние
    state_filename = "battle_state.json"
    battle.save_state(state_filename)
    print(f"💾 Состояние боя сохранено в файл: {state_filename}")


if __name__ == "__main__":
    main()
