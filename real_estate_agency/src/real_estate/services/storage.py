"""
Хранилище объектов недвижимости.

Отвечает только за хранение и поиск (SRP, глава 27).
Реализует магические методы, чтобы работать как список
(главы 31, 32).
"""

from collections.abc import Iterator
from typing import Any

from ..exceptions import ApartmentNotFoundError, PropertyAlreadyExistsError
from ..interfaces import Storage


class EstateStorage(Storage):
    """
    Хранилище объектов недвижимости.

    Хранит объекты в списке. Умеет искать по адресу.
    При поиске несуществующего объекта выбрасывает
    ApartmentNotFoundError.
    """

    def __init__(self) -> None:
        """Создаёт пустое хранилище объектов."""
        self._items: list[Any] = []

    def add(self, item: object) -> None:
        """Добавляет объект в хранилище."""
        address = getattr(item, "address", None)
        if address is not None and any(
            getattr(existing, "address", None) == address
            for existing in self._items
        ):
            raise PropertyAlreadyExistsError(address)
        self._items.append(item)

    def save(self, item: object) -> None:
        """Добавляет объект через интерфейс Storage."""
        self.add(item)

    def clear(self) -> None:
        """Удаляет все объекты из хранилища."""
        self._items.clear()

    def find_by_address(self, address: str) -> Any:
        """
        Ищет объект по адресу.

        Если объект найден, возвращает его.
        Если не найден, выбрасывает ApartmentNotFoundError.
        """
        for item in self._items:
            if getattr(item, "address", None) == address:
                return item
        raise ApartmentNotFoundError(address)

    def remove(self, item: object) -> None:
        """Удаляет объект из хранилища."""
        if item in self._items:
            self._items.remove(item)

    def list_all(self) -> list[Any]:
        """Возвращает копию списка всех объектов."""
        return list(self._items)

    def __len__(self) -> int:
        """Количество объектов в хранилище."""
        return len(self._items)

    def __iter__(self) -> Iterator[Any]:
        """Позволяет перебирать объекты в цикле for."""
        return iter(self._items)

    def __contains__(self, item: object) -> bool:
        """Позволяет использовать оператор in."""
        return item in self._items

    def __getitem__(self, index: int | slice) -> Any:
        """Позволяет обращаться по индексу."""
        return self._items[index]
