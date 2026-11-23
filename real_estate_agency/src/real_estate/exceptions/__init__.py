"""
Экспорт исключений.

Позволяет импортировать всё напрямую из пакета exceptions:

    from real_estate.exceptions import ApartmentNotFoundError
"""

from .errors import (
    AgencyError,
    ApartmentNotFoundError,
    ApartmentAlreadySoldError,
    ItemNotSellableError,
    PropertyAlreadyExistsError,
    ItemNotRentableError,
    ItemAlreadyRentedError,
    ItemNotRentedError,
    InvalidRentalPeriodError,
    InvalidAreaError,
    DatabaseError,
)

__all__ = [
    "AgencyError",
    "ApartmentNotFoundError",
    "ApartmentAlreadySoldError",
    "ItemNotSellableError",
    "PropertyAlreadyExistsError",
    "ItemNotRentableError",
    "ItemAlreadyRentedError",
    "ItemNotRentedError",
    "InvalidRentalPeriodError",
    "InvalidAreaError",
    "DatabaseError",
]
