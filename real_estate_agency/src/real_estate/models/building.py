"""
Здание.

Используется в композиции с классом Apartment:
квартира содержит объект Building как часть себя.
"""


from dataclasses import dataclass


@dataclass(slots=True)
class Building:
    """Здание — часть квартиры."""

    name: str
    floors: int

    def __post_init__(self) -> None:
        """Проверяет, что у здания есть название и этажи."""
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Название здания не может быть пустым")
        if not isinstance(self.floors, int) or isinstance(self.floors, bool):
            raise TypeError("Количество этажей должно быть целым числом")
        if self.floors < 1:
            raise ValueError("У здания должен быть хотя бы один этаж")

    def show(self) -> str:
        """Возвращает строковое описание здания."""
        return f"Здание {self.name!r}, {self.floors} этажей"

    def __repr__(self) -> str:
        """Возвращает однозначное представление здания."""
        return f"Building({self.name!r}, {self.floors})"
