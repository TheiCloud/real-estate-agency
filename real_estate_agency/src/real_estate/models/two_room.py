"""
Двухкомнатная квартира.

Наследник Apartment. Демонстрирует:
- полиморфизм (глава 4)
- разные наследники с общим родителем
"""

from dataclasses import dataclass

from .apartment import Apartment


@dataclass
class TwoRoom(Apartment):
    """Двухкомнатная квартира."""

    rooms: int = 2

    def get_info(self) -> str:
        """Переопределённое описание для двухкомнатной."""
        price = f"{self.price:,}".replace(",", " ")
        return (
            f"Двухкомнатная {self.address}: "
            f"{self.area} м², {self.rooms} комнаты, "
            f"{price} ₽"
        )

    def utility_cost(self) -> int:
        """Стоимость коммунальных услуг для двухкомнатной."""
        return 5000
