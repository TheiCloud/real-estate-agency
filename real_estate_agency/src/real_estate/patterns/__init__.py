"""
Экспорт всех паттернов.

Позволяет импортировать напрямую:

    from real_estate.patterns import EstateFactory, SingletonMeta
"""

from .factory import EstateFactory
from .singleton import SingletonMeta
from .decorator import (
    ItemDecorator,
    RenovatedDecorator,
    FurnishedDecorator,
    MortgageDecorator,
)
from .adapter import ApartmentAdapter

__all__ = [
    "EstateFactory",
    "SingletonMeta",
    "ItemDecorator",
    "RenovatedDecorator",
    "FurnishedDecorator",
    "MortgageDecorator",
    "ApartmentAdapter",
]
