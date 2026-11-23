"""
Адаптер для внешней системы учёта.

Паттерн Adapter (глава 39). Приводит словарь внешней
системы к интерфейсу Apartment: свойства address, area, price
и метод get_info().
"""

from typing import Any

from ..interfaces import Infoable


class ApartmentAdapter(Infoable):
    """
    Адаптер внешних данных к интерфейсу Apartment.

    Принимает словарь. Предоставляет свойства address, area, price.
    Поддерживает два набора ключей: внешний (location, size, cost)
    и внутренний (address, area, price).
    """

    def __init__(self, data: dict[str, Any]) -> None:
        """Принимает словарь с внешними или внутренними именами полей."""
        self._data = dict(data)
        if self.address is None or self.area is None or self.price is None:
            raise ValueError("Нужны адрес, площадь и цена объекта")

    def _value(self, external_key: str, internal_key: str) -> Any:
        """Возвращает значение по первому присутствующему ключу."""
        if external_key in self._data:
            return self._data[external_key]
        return self._data.get(internal_key)

    @property
    def address(self) -> str | None:
        """Адрес: из location или address."""
        return self._value("location", "address")

    @property
    def area(self) -> int | float | None:
        """Площадь: из size или area."""
        return self._value("size", "area")

    @property
    def price(self) -> int | float | None:
        """Цена: из cost или price."""
        return self._value("cost", "price")

    def get_info(self) -> str:
        """Описание в том же формате, что у Apartment."""
        price = f"{self.price:,}".replace(",", " ")
        return (
            f"Квартира {self.address}: "
            f"{self.area} м², {price} ₽"
        )
