class Inventory:
    """Класс инвентаря для хранения предметов"""

    def __init__(self, capacity=10):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        """Добавить предмет в инвентарь"""
        if len(self.items) < self.capacity:
            self.items.append(item)
            return True
        return False

    def remove_item(self, item):
        """Удалить предмет из инвентаря"""
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def use_item(self, item, target):
        """Использовать предмет на цели"""
        if item in self.items:
            result = item.use(target)
            if item.consumable:
                self.remove_item(item)
            return result
        return None

    def __len__(self):
        return len(self.items)

    def __contains__(self, item):
        return item in self.items

    def __iter__(self):
        return iter(self.items)
