"""
Экспорт интерфейсов и миксинов.

Позволяет импортировать всё напрямую из пакета interfaces:

    from real_estate.interfaces import Infoable, Notifier
"""

from .protocols import (
    Infoable,
    Sellable,
    Rentable,
    Renovatable,
    Describable,
    Notifier,
    Storage,
)
from .mixins import LoggableMixin, TimestampMixin

__all__ = [
    "Infoable",
    "Sellable",
    "Rentable",
    "Renovatable",
    "Describable",
    "Notifier",
    "Storage",
    "LoggableMixin",
    "TimestampMixin",
]
