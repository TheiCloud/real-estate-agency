"""
Тесты базы данных.
"""

import pytest

from real_estate.database import (
    DatabaseManager,
    ApartmentRepository,
    ClientRepository,
    DealRepository,
)
from real_estate.models import (
    Apartment,
    Studio,
    TwoRoom,
    House,
    Penthouse,
    Client,
)


# ─── DatabaseManager ───

def test_db_save_apartment(sample_db_path):
    """Квартира сохраняется в базу."""
    with DatabaseManager(sample_db_path) as db:
        flat = Apartment("ул. Ленина", 65, 8_500_000)
        row_id = db.save_apartment(flat)
        assert row_id > 0


def test_db_find_apartment(sample_db_path):
    """Квартира находится по адресу."""
    with DatabaseManager(sample_db_path) as db:
        flat = Apartment("ул. Ленина", 65, 8_500_000)
        db.save_apartment(flat)
        row = db.find_apartment("ул. Ленина")
        assert row is not None
        assert row["address"] == "ул. Ленина"
        assert row["area"] == 65


def test_db_find_nonexistent(sample_db_path):
    """Несуществующая квартира возвращает None."""
    with DatabaseManager(sample_db_path) as db:
        row = db.find_apartment("несуществующий")
        assert row is None


def test_db_save_updates_existing(sample_db_path):
    """Повторное сохранение обновляет запись."""
    with DatabaseManager(sample_db_path) as db:
        flat = Apartment("ул. Ленина", 65, 8_500_000)
        db.save_apartment(flat)

        flat2 = Apartment("ул. Ленина", 70, 9_000_000)
        db.save_apartment(flat2)

        row = db.find_apartment("ул. Ленина")
        assert row["area"] == 70


def test_db_persistence(sample_db_path):
    """Данные сохраняются между сессиями."""
    with DatabaseManager(sample_db_path) as db:
        db.save_apartment(Apartment("ул. Мира", 55, 6_000_000))

    with DatabaseManager(sample_db_path) as db:
        row = db.find_apartment("ул. Мира")
        assert row is not None
        assert row["area"] == 55


def test_db_delete(sample_db_path):
    """Удаление работает."""
    with DatabaseManager(sample_db_path) as db:
        db.save_apartment(Apartment("ул. Ленина", 65, 8_500_000))
        result = db.delete_apartment("ул. Ленина")
        assert result is True
        assert db.find_apartment("ул. Ленина") is None


def test_db_delete_nonexistent(sample_db_path):
    """Удаление несуществующей возвращает False."""
    with DatabaseManager(sample_db_path) as db:
        assert db.delete_apartment("несуществующий") is False


def test_db_save_client(sample_db_path):
    """Клиент сохраняется."""
    with DatabaseManager(sample_db_path) as db:
        row_id = db.save_client(Client("Иванов", 10_000_000))
        assert row_id > 0


# ─── ApartmentRepository ───

def test_repo_save_and_find(sample_db_path):
    """Репозиторий сохраняет и возвращает объект Apartment."""
    with DatabaseManager(sample_db_path) as db:
        repo = ApartmentRepository(db)
        repo.save(Apartment("ул. Ленина", 65, 8_500_000))

        found = repo.find_by_address("ул. Ленина")
        assert isinstance(found, Apartment)
        assert found.area == 65


def test_repo_find_all(sample_db_path):
    """find_all возвращает все объекты."""
    with DatabaseManager(sample_db_path) as db:
        repo = ApartmentRepository(db)
        repo.save(Apartment("ул. Ленина", 65, 8_500_000))
        repo.save(Apartment("ул. Садовая", 80, 12_000_000))

        all_items = repo.find_all()
        assert len(all_items) == 2


def test_repository_round_trips_all_estate_types(sample_db_path):
    """SQLite сохраняет конкретный тип, поля и статусы объектов."""
    items = [
        Apartment("A", 60, 8_000_000),
        Studio("B", 25, 4_000_000, kitchen_area=6),
        TwoRoom("C", 70, 9_000_000, rooms=3),
        Penthouse("D", 150, 50_000_000, terrace=30),
        House("E", 200, 2, price=18_000_000),
    ]
    items[0].is_sold = True
    items[1].is_rented = True
    with DatabaseManager(sample_db_path) as db:
        repo = ApartmentRepository(db)
        for item in items:
            repo.save(item)
        restored = repo.find_all()

    assert [type(item) for item in restored] == [type(item) for item in items]
    assert restored[0].is_sold is True
    assert restored[1].is_rented is True
    assert restored[1].kitchen_area == 6
    assert restored[2].rooms == 3
    assert restored[3].terrace == 30
    assert restored[4].floors == 2
    assert restored[4].price == 18_000_000


def test_repo_delete(sample_db_path):
    """Репозиторий удаляет объекты."""
    with DatabaseManager(sample_db_path) as db:
        repo = ApartmentRepository(db)
        repo.save(Apartment("ул. Ленина", 65, 8_500_000))
        assert repo.delete("ул. Ленина") is True


# ─── ClientRepository ───

def test_client_repo_save(sample_db_path):
    """ClientRepository сохраняет клиента."""
    with DatabaseManager(sample_db_path) as db:
        repo = ClientRepository(db)
        row_id = repo.save(Client("Иванов", 10_000_000))
        assert row_id > 0


def test_client_repository_loads_records(sample_db_path):
    """Репозиторий восстанавливает клиентов из SQLite."""
    with DatabaseManager(sample_db_path) as db:
        repo = ClientRepository(db)
        repo.save(Client("Иванов", 10_000_000))
        clients = repo.find_all()
    assert len(clients) == 1
    assert clients[0].name == "Иванов"
    assert clients[0].budget == 10_000_000


# ─── DealRepository ───

def test_deal_repo_save(sample_db_path):
    """DealRepository сохраняет сделку."""
    with DatabaseManager(sample_db_path) as db:
        db.save_apartment(Apartment("ул. Ленина", 65, 8_500_000))
        row = db.find_apartment("ул. Ленина")

        repo = DealRepository(db)
        deal_id = repo.save({
            "apartment_id": row["id"],
            "client_id": None,
            "agent_id": None,
            "commission": 255_000,
            "date": "2025-01-15",
        })
        assert deal_id > 0
