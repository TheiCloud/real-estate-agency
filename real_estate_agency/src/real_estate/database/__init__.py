"""
Экспорт компонентов базы данных.

Позволяет импортировать напрямую:

    from real_estate.database import DatabaseManager, ApartmentRepository
"""

from .manager import DatabaseManager
from .repositories import (
    ApartmentRepository,
    ClientRepository,
    DealRepository,
)

__all__ = [
    "DatabaseManager",
    "ApartmentRepository",
    "ClientRepository",
    "DealRepository",
]
