"""
Точка входа проекта.

Запуск:

    python main.py

Демонстрирует работу всех ключевых возможностей:
фабрику, хранилище, уведомления, сделки, отчёты,
декораторы, адаптер, исключения.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from real_estate.patterns import (
    EstateFactory,
    ApartmentAdapter,
    RenovatedDecorator,
    FurnishedDecorator,
)
from real_estate.services import (
    EstateStorage,
    DealService,
    NotificationService,
    ReportService,
    EmailNotifier,
    PercentCommission,
    FixedCommission,
    LoyaltyCommission,
    CommissionCalculator,
)
from real_estate.models import Client, Apartment, Building
from real_estate.exceptions import ApartmentNotFoundError


def section(title: str) -> None:
    """Печатает заголовок раздела."""
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def main() -> None:
    """Основная демонстрация проекта."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    section("1. Фабрика создаёт объекты")

    flat = EstateFactory.create(
        "apartment",
        address="ул. Ленина, д. 10, кв. 5",
        area=65,
        price=8_500_000,
        building=Building("Дом на Ленина", 9),
    )
    studio = EstateFactory.create(
        "studio",
        address="ул. Пушкина, д. 1, кв. 7",
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
    penthouse = EstateFactory.create(
        "penthouse",
        address="ул. Мира, д. 1, кв. 100",
        area=150,
        price=50_000_000,
        terrace=30,
    )

    for item in [flat, studio, house, penthouse]:
        print(f"  {item.get_info()}")

    section("2. Хранилище")

    storage = EstateStorage()
    for item in [flat, studio, house, penthouse]:
        storage.add(item)

    print(f"  Добавлено объектов: {len(storage)}")

    found = storage.find_by_address("ул. Ленина, д. 10, кв. 5")
    print(f"  Найдено: {found.get_info()}")
    print(f"  Композиция: {flat.building.show()}")

    section("3. Уведомления (Observer)")

    notifier = NotificationService()
    client = Client("Иванов", 10_000_000)
    notifier.subscribe(client)
    print(f"  Подписчиков: {notifier.count()}")

    section("4. Продажа квартиры (Strategy)")

    deal_service = DealService(
        storage, EmailNotifier(), PercentCommission()
    )
    result = deal_service.sell("ул. Ленина, д. 10, кв. 5", "Петров")
    print(f"  Покупатель: {result['buyer']}")
    print(f"  Комиссия: {result['commission']:,.0f} ₽".replace(",", " "))

    section("5. Отчёт")

    reports = ReportService()
    print(reports.generate(storage, "Дом-Сервис"))

    section("6. Декораторы")

    decorated = RenovatedDecorator(FurnishedDecorator(flat))
    print(f"  {decorated.get_info()}")

    section("7. Адаптер")

    external = ApartmentAdapter({
        "location": "ул. Гагарина, д. 5",
        "size": 70,
        "cost": 7_500_000,
    })
    print(f"  {external.get_info()}")

    section("8. Собственные исключения")

    try:
        storage.find_by_address("несуществующий адрес")
    except ApartmentNotFoundError as e:
        print(f"  Поймано: {e}")

    section("9. Классовый счётчик")

    print(f"  Всего квартир: {Apartment.count}")

    section("10. Стратегии комиссии")

    price = 8_500_000
    for strategy in [
        FixedCommission(),
        PercentCommission(),
        LoyaltyCommission(),
    ]:
        commission = strategy.calculate(price)
        name = strategy.__class__.__name__
        print(f"  {name}: {commission:,.0f} ₽".replace(",", " "))

    calculator = CommissionCalculator(PercentCommission)
    print(
        f"  Вызов калькулятора: "
        f"{calculator(price):,.0f} ₽".replace(",", " ")
    )

    section("ГОТОВО")


if __name__ == "__main__":
    main()
