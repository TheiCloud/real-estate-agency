"""
Дом.

Отдельный тип недвижимости (не квартира).
Демонстрирует:
- наследование от EstateItem (глава 3)
- интерфейс Sellable (глава 40)
- @dataclass (глава 20)
"""

from dataclasses import asdict, dataclass, field

from ..interfaces import Sellable
from ..utils import EstateUtils
from .estate_item import EstateItem


@dataclass
class House(EstateItem, Sellable):
    """Жилой дом."""

    address: str
    area: int
    floors: int
    price: int = 0
    is_sold: bool = field(default=False, init=False)

    def get_info(self) -> str:
        """Описание дома."""
        price = f"{self.price:,}".replace(",", " ")
        return (
            f"Дом {self.address}: "
            f"{self.area} м², {self.floors} этажей, {price} ₽"
        )

    def __post_init__(self) -> None:
        """Проверяет обязательные характеристики дома."""
        if not EstateUtils.is_valid_address(self.address):
            raise ValueError("Адрес не может быть пустым")
        if not EstateUtils.is_valid_area(self.area):
            raise ValueError("Площадь должна быть от 5 до 500 м²")
        if not isinstance(self.floors, int) or isinstance(self.floors, bool):
            raise TypeError("Количество этажей должно быть целым числом")
        if self.floors < 1:
            raise ValueError("У дома должен быть хотя бы один этаж")
        if not isinstance(self.price, int) or isinstance(self.price, bool):
            raise TypeError("Цена дома должна быть целым числом")
        if self.price < 0:
            raise ValueError("Цена не может быть отрицательной")

    def sell(self) -> str:
        """Продаёт дом."""
        if self.is_sold:
            return "Уже продан"
        self.is_sold = True
        return "Дом продан"

    def utility_cost(self) -> int:
        """Стоимость коммунальных услуг для дома."""
        return 7000

    def to_dict(self) -> dict:
        """Преобразует дом в словарь для хранения."""
        data = asdict(self)
        data["type"] = self.__class__.__name__
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "House":
        """Создаёт дом из словаря базы данных."""
        house = cls(
            address=data["address"],
            area=data["area"],
            floors=data["floors"],
            price=data.get("price", 0),
        )
        house.is_sold = bool(data.get("is_sold", False))
        return house
