"""
Пентхаус.

Наследник Apartment. Демонстрирует:
- расширение метода через super() (глава 9)
- добавление поля в @dataclass (глава 20)
"""

from dataclasses import dataclass

from .apartment import Apartment


@dataclass
class Penthouse(Apartment):
    """Пентхаус — квартира с террасой."""

    terrace: int = 0

    def get_info(self) -> str:
        """Дополняет родительское описание информацией о террасе."""
        parent_info = super().get_info()
        return f"{parent_info} + терраса {self.terrace} м²"
