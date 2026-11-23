"""
Демо сервисов и паттернов.

Запуск:

    python examples/demo_services.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from real_estate.patterns import (
    EstateFactory,
    ApartmentAdapter,
    RenovatedDecorator,
    FurnishedDecorator,
)
from real_estate.services import (
    EstateStorage,
    DealService,
    RentalService,
    NotificationService,
    ReportService,
    EmailNotifier,
    SmsNotifier,
    PercentCommission,
    FixedCommission,
    LoyaltyCommission,
)
from real_estate.models import Client


def main() -> None:
    """Демонстрирует сервисы и паттерны на нескольких объектах."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    """Демонстрация сервисов и паттернов."""

    print("=== Фабрика ===")

    flat = EstateFactory.create(
        "apartment",
        address="ул. Ленина, д. 10",
        area=65,
        price=8_500_000,
    )
    studio = EstateFactory.create(
        "studio",
        address="ул. Пушкина, д. 1",
        area=25,
        price=4_000_000,
    )
    house = EstateFactory.create(
        "house",
        address="ул. Садовая, д. 3",
        area=200,
        floors=2,
        price=18_000_000,
    )

    for item in [flat, studio, house]:
        print(f"  {item.get_info()}")

    print()
    print("=== Хранилище ===")

    storage = EstateStorage()
    for item in [flat, studio, house]:
        storage.add(item)
    print(f"  Всего объектов: {len(storage)}")

    print()
    print("=== Observer: подписка ===")

    notifier = NotificationService()
    client = Client("Иванов", 10_000_000)
    notifier.subscribe(client)
    print(f"  Подписчиков: {notifier.count()}")

    print()
    print("=== Продажа квартиры ===")

    deal_service = DealService(
        storage, EmailNotifier(), PercentCommission()
    )
    result = deal_service.sell("ул. Ленина, д. 10", "Петров")
    print(f"  Комиссия: {result['commission']:,.0f} ₽".replace(",", " "))

    print()
    print("=== Аренда студии ===")

    rental_service = RentalService(storage, SmsNotifier())
    result = rental_service.rent("ул. Пушкина, д. 1", "Сидоров", 30)
    print(f"  Арендатор: {result['tenant']}, дней: {result['days']}")

    print()
    print("=== Отчёт ===")

    reports = ReportService()
    print(reports.generate(storage, "Дом-Сервис"))

    print()
    print("=== Декораторы ===")

    decorated = RenovatedDecorator(FurnishedDecorator(studio))
    print(f"  {decorated.get_info()}")

    print()
    print("=== Адаптер ===")

    external = ApartmentAdapter({
        "location": "ул. Гагарина, д. 5",
        "size": 70,
        "cost": 7_500_000,
    })
    print(f"  {external.get_info()}")

    print()
    print("=== Стратегии комиссии ===")

    price = 8_500_000
    for strategy in [
        FixedCommission(),
        PercentCommission(),
        LoyaltyCommission(),
    ]:
        commission = strategy.calculate(price)
        name = strategy.__class__.__name__
        print(f"  {name}: {commission:,.0f} ₽".replace(",", " "))


if __name__ == "__main__":
    main()
