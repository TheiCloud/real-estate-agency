"""
Студия.

Наследник Apartment. Демонстрирует:
- наследование (глава 3)
- переопределение метода (глава 9)
- @dataclass с дополнительным полем (глава 20)
"""

from dataclasses import dataclass

from .apartment import Apartment


@dataclass
class Studio(Apartment):
    """Студия — квартира с маленькой кухней."""

    kitchen_area: int = 5

    def get_info(self) -> str:
        """Переопределённое описание для студии."""
        price = f"{self.price:,}".replace(",", " ")
        return (
            f"Студия {self.address}: "
            f"{self.area} м² (кухня {self.kitchen_area} м²), "
            f"{price} ₽"
        )

    def utility_cost(self) -> int:
        """Стоимость коммунальных услуг для студии."""
        return 3000
