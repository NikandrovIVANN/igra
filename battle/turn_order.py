class TurnOrder:
    """Итератор для определения порядка ходов на основе ловкости"""

    def __init__(self, participants):
        self.participants = participants
        self.current_turn = 0

    def __iter__(self):
        return self

    def __next__(self):
        # Фильтруем живых участников
        alive_participants = [p for p in self.participants if p.is_alive]

        if not alive_participants:
            raise StopIteration

        # Сортируем по ловкости (в порядке убывания)
        alive_participants.sort(key=lambda x: x.agility, reverse=True)

        if self.current_turn >= len(alive_participants):
            self.current_turn = 0

        participant = alive_participants[self.current_turn]
        self.current_turn += 1

        return participant