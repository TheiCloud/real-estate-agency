"""
Полное демо: модели, сервисы, паттерны, база данных.

Запуск:

    python examples/demo_full.py
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
    NotificationService,
    ReportService,
    EmailNotifier,
    PercentCommission,
)
from real_estate.database import DatabaseManager, ApartmentRepository
from real_estate.models import Client


def main() -> None:
    """Показывает полный сценарий с сохранением и загрузкой SQLite."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    """Полная демонстрация проекта."""

    db_path = "data/demo_full.db"

    print("=== 1. Создание объектов через фабрику ===")

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
    print("=== 2. Добавление в хранилище ===")

    storage = EstateStorage()
    for item in [flat, studio, house]:
        storage.add(item)
    print(f"  Объектов: {len(storage)}")

    print()
    print("=== 3. Подписка клиента ===")

    notifier = NotificationService()
    client = Client("Иванов", 10_000_000)
    notifier.subscribe(client)
    print(f"  Подписчиков: {notifier.count()}")

    print()
    print("=== 4. Продажа ===")

    deal_service = DealService(
        storage, EmailNotifier(), PercentCommission()
    )
    result = deal_service.sell("ул. Ленина, д. 10", "Петров")
    print(f"  Комиссия: {result['commission']:,.0f} ₽".replace(",", " "))

    print()
    print("=== 5. Декораторы ===")

    decorated = RenovatedDecorator(FurnishedDecorator(studio))
    print(f"  {decorated.get_info()}")

    print()
    print("=== 6. Адаптер ===")

    external = ApartmentAdapter({
        "location": "ул. Гагарина, д. 5",
        "size": 70,
        "cost": 7_500_000,
    })
    print(f"  {external.get_info()}")

    print()
    print("=== 7. Сохранение в базу ===")

    with DatabaseManager(db_path) as db:
        repo = ApartmentRepository(db)
        for item in storage:
            repo.save(item)
    print(f"  Сохранено: {len(storage)}")

    print()
    print("=== 8. Симуляция перезапуска ===")

    storage = EstateStorage()
    print("  Хранилище очищено")

    print()
    print("=== 9. Загрузка из базы ===")

    with DatabaseManager(db_path) as db:
        repo = ApartmentRepository(db)
        items = repo.find_all()
        for item in items:
            storage.add(item)
    print(f"  Загружено: {len(storage)}")

    print()
    print("=== 10. Отчёт по загруженным объектам ===")

    reports = ReportService()
    print(reports.generate(storage, "Дом-Сервис"))


if __name__ == "__main__":
    main()
