"""
Сервис оформления сделок.

Отвечает только за сделки (SRP, глава 27).
Зависит от абстракций: Storage, Notifier, CommissionStrategy (DIP, глава 40).
"""

from ..interfaces import Sellable, Notifier, Storage
from ..exceptions import (
    ApartmentAlreadySoldError,
    ItemNotSellableError,
)
from .commission import CommissionStrategy


class DealService:
    """
    Сервис оформления сделок.

    Зависимости передаются через конструктор. Сервис не создаёт
    их сам: это позволяет подменять реализации.
    """

    def __init__(
        self,
        storage: Storage,
        notifier: Notifier,
        commission: CommissionStrategy | None = None,
    ) -> None:
        """Сохраняет зависимости сервиса сделок."""
        self.storage = storage
        self.notifier = notifier
        self.commission = commission

    def sell(self, address: str, buyer: str) -> dict[str, object]:
        """
        Продаёт объект недвижимости по адресу.

        Шаги:
        1. Найти объект в хранилище.
        2. Проверить, что он не продан.
        3. Проверить, что он продаётся (интерфейс Sellable).
        4. Пометить проданным.
        5. Рассчитать комиссию (если стратегия задана).
        6. Отправить уведомление.
        7. Вернуть информацию о сделке.
        """
        item = self.storage.find_by_address(address)

        if getattr(item, "is_sold", False):
            raise ApartmentAlreadySoldError(address)

        if not isinstance(item, Sellable):
            raise ItemNotSellableError(f"{address} не продаётся")

        price = getattr(item, "price", None)
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError(f"Для продажи {address} нужна цена больше нуля")

        item.sell()
        item.is_sold = True

        commission = (
            self.commission.calculate(price)
            if self.commission else 0
        )

        self.notifier.send(f"Продано: {address} → {buyer}")

        return {
            "item": item,
            "buyer": buyer,
            "commission": commission,
        }
