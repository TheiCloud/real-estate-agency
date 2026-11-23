"""
Базовый класс недвижимости.

EstateItem — абстрактный класс. Объект создать нельзя,
но любой наследник обязан реализовать get_info().
"""

from abc import ABC

from ..interfaces import Infoable


class EstateItem(Infoable, ABC):
    """Общий интерфейс для всех объектов недвижимости."""

    def describe(self) -> str:
        """Возвращает описание. Нужен для утиной типизации."""
        return self.get_info()

    def __repr__(self) -> str:
        """Возвращает класс и описание объекта недвижимости."""
        return f"{self.__class__.__name__}({self.get_info()!r})"
