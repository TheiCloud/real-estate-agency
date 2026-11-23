"""
Декораторы для меток объектов недвижимости.

Паттерн Decorator (глава 38). Позволяет добавлять метки
к объекту без изменения его класса. Декораторы
комбинируются в цепочку.
"""

from ..interfaces import Infoable


class ItemDecorator(Infoable):
    """
    Базовый декоратор.

    Содержит обёрнутый объект и делегирует ему вызов
    get_info(). Наследники дополняют результат.
    """

    def __init__(self, item: Infoable) -> None:
        """Сохраняет объект, которому делегируются вызовы."""
        self.item = item

    def get_info(self) -> str:
        """Делегирует работу обёрнутому объекту."""
        return self.item.get_info()


class RenovatedDecorator(ItemDecorator):
    """Добавляет метку «с ремонтом»."""

    def get_info(self) -> str:
        """Добавляет метку о ремонте к описанию объекта."""
        return f"{self.item.get_info()} (с ремонтом)"


class FurnishedDecorator(ItemDecorator):
    """Добавляет метку «с мебелью»."""

    def get_info(self) -> str:
        """Добавляет метку о мебели к описанию объекта."""
        return f"{self.item.get_info()} (с мебелью)"


class MortgageDecorator(ItemDecorator):
    """Добавляет метку «ипотека возможна»."""

    def get_info(self) -> str:
        """Добавляет метку о возможности ипотеки."""
        return f"{self.item.get_info()} (ипотека возможна)"
