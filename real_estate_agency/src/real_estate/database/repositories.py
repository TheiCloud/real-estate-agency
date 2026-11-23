"""
Репозитории для работы с сущностями.

Репозиторий — это слой между бизнес-логикой и базой данных.
Он скрывает SQL и предоставляет удобный интерфейс для работы
с объектами домена (SRP, глава 27).
"""

import json
import sqlite3
from typing import Any

from ..models import Apartment, Studio, TwoRoom, House, Penthouse, Client


_ITEM_TYPES = {
    model.__name__: model
    for model in (Apartment, Studio, TwoRoom, House, Penthouse)
}


def _item_from_row(row: sqlite3.Row) -> Any:
    """Восстанавливает класс недвижимости из строки базы данных."""
    keys = set(row.keys())
    if "payload" in keys:
        data = json.loads(row["payload"] or "{}")
    else:
        data = {}
    for key in ("address", "area", "price", "type", "is_sold", "is_rented"):
        if key in keys:
            data.setdefault(key, row[key])
    model = _ITEM_TYPES.get(data.get("type", "Apartment"), Apartment)
    return model.from_dict(data)


class ApartmentRepository:
    """
    Репозиторий квартир.

    Сохраняет, ищет и удаляет квартиры через DatabaseManager.
    """

    def __init__(self, manager: Any) -> None:
        """Связывает репозиторий с активным DatabaseManager."""
        self.manager = manager

    def save(self, apartment: Any) -> int:
        """Сохраняет квартиру в базу."""
        return self.manager.save_apartment(apartment)

    def find_by_address(self, address: str) -> Any | None:
        """Возвращает сохранённый объект или None."""
        row = self.manager.find_apartment(address)
        if row is None:
            return None
        return _item_from_row(row)

    def find_all(self) -> list[Any]:
        """Возвращает список всех квартир."""
        rows = self.manager.find_all_apartments()
        return [_item_from_row(row) for row in rows]

    def delete(self, address: str) -> bool:
        """Удаляет квартиру по адресу."""
        return self.manager.delete_apartment(address)


class ClientRepository:
    """
    Репозиторий клиентов.

    Сохраняет и ищет клиентов.
    """

    def __init__(self, manager: Any) -> None:
        """Связывает репозиторий клиентов с активной базой."""
        self.manager = manager

    def save(self, client: Client) -> int:
        """Сохраняет клиента."""
        return self.manager.save_client(client)

    def find_all(self) -> list[Client]:
        """Загружает всех клиентов."""
        return [
            Client(row["name"], row["budget"])
            for row in self.manager.find_all_clients()
        ]


class DealRepository:
    """
    Репозиторий сделок.

    Сохраняет сделки.
    """

    def __init__(self, manager: Any) -> None:
        """Связывает репозиторий сделок с активной базой."""
        self.manager = manager

    def save(self, deal: dict[str, Any]) -> int:
        """Сохраняет сделку."""
        return self.manager.save_deal(deal)
