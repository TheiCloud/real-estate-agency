"""
Базовое демо: модели и хранилище.

Запуск:

    python examples/demo_basic.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from real_estate.models import Apartment, House, Studio
from real_estate.services import EstateStorage
from real_estate.exceptions import ApartmentNotFoundError


def main() -> None:
    """Демонстрация моделей и хранилища."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print("=== Создание объектов ===")

    flat = Apartment("ул. Ленина, д. 10, кв. 5", 65, 8_500_000)
    studio = Studio("ул. Пушкина, д. 1, кв. 7", 25, 4_000_000)
    house = House("ул. Садовая, д. 3", 200, 2, price=18_000_000)

    print(flat.get_info())
    print(studio.get_info())
    print(house.get_info())

    print()
    print("=== Хранилище ===")

    storage = EstateStorage()
    storage.add(flat)
    storage.add(studio)
    storage.add(house)

    print(f"Всего объектов: {len(storage)}")

    print()
    print("=== Перебор ===")

    for item in storage:
        print(f"  {item.get_info()}")

    print()
    print("=== Поиск ===")

    found = storage.find_by_address("ул. Пушкина, д. 1, кв. 7")
    print(f"Найдено: {found.get_info()}")

    print()
    print("=== Обработка ошибки ===")

    try:
        storage.find_by_address("несуществующий адрес")
    except ApartmentNotFoundError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
