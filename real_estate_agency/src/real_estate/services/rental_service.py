"""
Сервис аренды.

Отвечает только за аренду (SRP, глава 27).
Отделён от DealService, потому что продажа и аренда —
разные бизнес-операции.
"""

from ..interfaces import Rentable, Notifier, Storage
from ..exceptions import (
    ApartmentAlreadySoldError,
    InvalidRentalPeriodError,
    ItemAlreadyRentedError,
    ItemNotRentedError,
    ItemNotRentableError,
)


class RentalService:
    """
    Сервис аренды недвижимости.

    Зависимости передаются через конструктор (DIP, глава 40).
    """

    def __init__(self, storage: Storage, notifier: Notifier) -> None:
        """Сохраняет хранилище и отправитель уведомлений."""
        self.storage = storage
        self.notifier = notifier

    def rent(self, address: str, tenant: str, days: int) -> dict[str, object]:
        """
        Сдаёт объект в аренду.

        Шаги:
        1. Найти объект.
        2. Проверить, что он сдаётся (Rentable).
        3. Пометить как арендованный.
        4. Отправить уведомление.
        5. Вернуть информацию об аренде.
        """
        if not isinstance(days, int) or isinstance(days, bool) or days < 1:
            raise InvalidRentalPeriodError()

        item = self.storage.find_by_address(address)

        if getattr(item, "is_sold", False):
            raise ApartmentAlreadySoldError(address)

        if not isinstance(item, Rentable):
            raise ItemNotRentableError(f"{address} не сдаётся")

        if getattr(item, "is_rented", False):
            raise ItemAlreadyRentedError(f"{address} уже сдан")

        item.rent()
        item.is_rented = True

        self.notifier.send(
            f"Сдано в аренду: {address} → {tenant} на {days} дней"
        )

        return {
            "item": item,
            "tenant": tenant,
            "days": days,
        }

    def return_item(self, address: str) -> dict[str, object]:
        """
        Возвращает объект из аренды.

        Помечает объект как доступный.
        """
        item = self.storage.find_by_address(address)
        if not isinstance(item, Rentable):
            raise ItemNotRentableError(f"{address} не сдаётся")
        if not getattr(item, "is_rented", False):
            raise ItemNotRentedError(f"{address} не находится в аренде")
        item.is_rented = False

        self.notifier.send(f"Возвращено из аренды: {address}")

        return {"item": item}
