"""
Экспорт всех моделей проекта.

Позволяет импортировать всё напрямую:

    from real_estate.models import Apartment, Studio, House
"""

from .building import Building
from .estate_item import EstateItem
from .apartment import Apartment
from .studio import Studio
from .two_room import TwoRoom
from .house import House
from .penthouse import Penthouse
from .client import Client, Agent

__all__ = [
    "Building",
    "EstateItem",
    "Apartment",
    "Studio",
    "TwoRoom",
    "House",
    "Penthouse",
    "Client",
    "Agent",
]
