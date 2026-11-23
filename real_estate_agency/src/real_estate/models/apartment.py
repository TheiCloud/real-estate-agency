"""
Квартира.

Главная модель проекта. Демонстрирует:
- @dataclass (глава 20)
- миксин LoggableMixin (глава 20)
- интерфейсы Sellable, Rentable (глава 40)
- классовый счётчик count (глава 16)
- __post_init__ (глава 20)
- __str__ (глава 11)
- классовый метод from_dict (глава 15)
"""

from dataclasses import asdict, dataclass, field, fields
from typing import ClassVar

from ..interfaces import LoggableMixin, Sellable, Rentable, Renovatable
from ..utils import EstateUtils, RangeDescriptor
from .building import Building
from .estate_item import EstateItem


@dataclass
class Apartment(
    EstateItem,
    LoggableMixin,
    Sellable,
    Rentable,
    Renovatable,
):
    """Квартира: продаётся и сдаётся в аренду."""

    address: str
    area: int
    price: int
    building: Building | None = field(default=None, repr=False, compare=False)

    count: ClassVar[int] = 0
    is_sold: bool = field(default=False, init=False)
    is_rented: bool = field(default=False, init=False)
    is_renovated: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        """Вызывается после автоматического __init__."""
        if not EstateUtils.is_valid_address(self.address):
            raise ValueError("Адрес не может быть пустым")
        type(self).count += 1

    def get_info(self) -> str:
        """Возвращает текстовое описание квартиры."""
        price = f"{self.price:,}".replace(",", " ")
        return (
            f"Квартира {self.address}: "
            f"{self.area} м², {price} ₽"
        )

    def sell(self) -> str:
        """Продаёт квартиру."""
        if self.is_sold:
            return "Уже продана"
        self.is_sold = True
        return "Продано"

    def rent(self) -> str:
        """Сдаёт квартиру в аренду."""
        return "Сдано"

    def renovate(self) -> str:
        """Отмечает квартиру как прошедшую ремонт."""
        self.is_renovated = True
        return "Ремонт завершён"

    def to_dict(self) -> dict:
        """Преобразует объект в словарь для сохранения в БД."""
        data = asdict(self)
        data["type"] = self.__class__.__name__
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Apartment":
        """Создаёт объект из словаря при загрузке из БД."""
        init_fields = {item.name for item in fields(cls) if item.init}
        values = {
            key: data[key] for key in init_fields if key in data
        }
        building = values.get("building")
        if isinstance(building, dict):
            values["building"] = Building(**building)
        instance = cls(**values)
        instance.is_sold = bool(data.get("is_sold", False))
        instance.is_rented = bool(data.get("is_rented", False))
        instance.is_renovated = bool(data.get("is_renovated", False))
        return instance

    def __str__(self) -> str:
        """Возвращает краткое описание квартиры."""
        return self.get_info()


# Assign after @dataclass so these remain required constructor arguments.
# Dataclass-generated __init__ still routes assignments through the descriptor.
Apartment.area = RangeDescriptor(5, 500)
Apartment.area.__set_name__(Apartment, "area")
Apartment.price = RangeDescriptor(1, 10**15)
Apartment.price.__set_name__(Apartment, "price")
