"""
Тесты моделей.

Проверяют создание объектов, работу методов,
классовый счётчик, сериализацию.
"""

import pytest
import copy

from real_estate.models import (
    Apartment, Studio, TwoRoom, House, Penthouse, Building,
    Client, Agent,
)


# ─── Apartment ───

def test_apartment_creation():
    """Квартира создаётся с правильными полями."""
    flat = Apartment("ул. Ленина", 65, 8_500_000)
    assert flat.address == "ул. Ленина"
    assert flat.area == 65
    assert flat.price == 8_500_000
    assert flat.is_sold is False


def test_apartment_get_info():
    """Метод get_info возвращает описание."""
    flat = Apartment("ул. Ленина", 65, 8_500_000)
    info = flat.get_info()
    assert "ул. Ленина" in info
    assert "65" in info


def test_apartment_sell():
    """Метод sell помечает квартиру как проданную."""
    flat = Apartment("ул. Ленина", 65, 8_500_000)
    result = flat.sell()
    assert result == "Продано"
    assert flat.is_sold is True


def test_apartment_sell_twice():
    """Повторная продажа возвращает «Уже продана»."""
    flat = Apartment("ул. Ленина", 65, 8_500_000)
    flat.sell()
    result = flat.sell()
    assert result == "Уже продана"


def test_apartment_rent():
    """Метод rent возвращает «Сдано»."""
    flat = Apartment("ул. Ленина", 65, 8_500_000)
    assert flat.rent() == "Сдано"


def test_apartment_renovate():
    """Ремонт реализует контракт Renovatable."""
    flat = Apartment("ул. Ленина", 65, 8_500_000)
    assert flat.renovate() == "Ремонт завершён"
    assert flat.is_renovated is True


def test_apartment_count():
    """Классовый счётчик увеличивается при создании."""
    Apartment.count = 0
    Apartment("а", 50, 5_000_000)
    Apartment("б", 60, 6_000_000)
    assert Apartment.count == 2


def test_apartment_to_dict():
    """Метод to_dict возвращает словарь с нужными ключами."""
    flat = Apartment("ул. Ленина", 65, 8_500_000)
    data = flat.to_dict()
    assert data["address"] == "ул. Ленина"
    assert data["area"] == 65
    assert data["price"] == 8_500_000
    assert data["type"] == "Apartment"


def test_apartment_from_dict():
    """Метод from_dict создаёт квартиру из словаря."""
    data = {"address": "ул. Мира", "area": 55, "price": 6_000_000}
    flat = Apartment.from_dict(data)
    assert flat.address == "ул. Мира"
    assert flat.area == 55


def test_apartment_rejects_invalid_dimensions_and_address():
    """Дескриптор и валидация адреса отклоняют неверные данные."""
    with pytest.raises(ValueError):
        Apartment("ул. Ленина", 4, 100_000)
    with pytest.raises(ValueError):
        Apartment("ул. Ленина", 65, 0)
    with pytest.raises(ValueError):
        Apartment("  ", 65, 100_000)


def test_apartment_building_composition_round_trip():
    """Квартира содержит Building и восстанавливает его из словаря."""
    building = Building("Дом на Невском", 12)
    apartment = Apartment("Невский, 1", 65, 8_500_000, building=building)
    restored = Apartment.from_dict(apartment.to_dict())
    assert restored.building == building
    assert restored.building is not building


def test_apartment_copy_and_dataclass_equality(sample_apartment):
    """Модели поддерживают сравнение и копирование стандартной библиотекой."""
    shallow = copy.copy(sample_apartment)
    deep = copy.deepcopy(sample_apartment)
    assert shallow == sample_apartment
    assert deep == sample_apartment
    assert shallow is not sample_apartment
    assert deep is not sample_apartment


def test_apartment_string_representation(sample_apartment):
    """str() возвращает понятное описание объекта."""
    assert str(sample_apartment) == sample_apartment.get_info()


# ─── Studio ───

def test_studio():
    """Студия создаётся с kitchen_area и своей коммуналкой."""
    studio = Studio("ул. Пушкина", 25, 4_000_000, kitchen_area=6)
    assert studio.kitchen_area == 6
    assert studio.utility_cost() == 3000


def test_studio_default_kitchen():
    """Значение kitchen_area по умолчанию — 5."""
    studio = Studio("ул. Пушкина", 25, 4_000_000)
    assert studio.kitchen_area == 5


# ─── TwoRoom ───

def test_two_room():
    """Двухкомнатная имеет 2 комнаты и коммуналку 5000."""
    flat = TwoRoom("ул. Ленина", 65, 8_500_000)
    assert flat.rooms == 2
    assert flat.utility_cost() == 5000


# ─── House ───

def test_house():
    """Дом создаётся с этажами и коммуналкой 7000."""
    house = House("ул. Садовая", 200, 2)
    assert house.floors == 2
    assert house.utility_cost() == 7000


def test_house_sell():
    """Дом продаётся."""
    house = House("ул. Садовая", 200, 2)
    assert house.sell() == "Дом продан"


# ─── Penthouse ───

def test_penthouse():
    """Пентхаус содержит террасу и расширяет описание."""
    penthouse = Penthouse("ул. Мира", 150, 50_000_000, terrace=30)
    assert penthouse.terrace == 30
    info = penthouse.get_info()
    assert "терраса" in info
    assert "30" in info


# ─── Client и Agent ───

def test_client_describe():
    """Клиент описывает себя."""
    client = Client("Иванов", 10_000_000)
    assert "Иванов" in client.describe()


def test_client_update():
    """Клиент получает уведомление."""
    client = Client("Иванов")
    client.update("Новая квартира")
    assert len(client.notifications) == 1


def test_client_notifications_isolated():
    """Списки уведомлений не смешиваются между клиентами."""
    client1 = Client("Иванов")
    client2 = Client("Петров")
    client1.update("Событие")
    assert len(client1.notifications) == 1
    assert len(client2.notifications) == 0


def test_agent_describe():
    """Агент описывает себя."""
    agent = Agent("Петров", 5)
    assert "Петров" in agent.describe()
    assert "5" in agent.describe()


# ─── Building ───

def test_building():
    """Здание описывает себя."""
    building = Building("Дом-1", 9)
    assert "Дом-1" in building.show()
    assert "9" in building.show()


# ─── Утиная типизация ───

def test_describe_item_duck_typing():
    """Функция работает с любым объектом с describe()."""
    def describe_item(item):
        """Возвращает описание переданного объекта."""
        return item.describe()

    assert "Иванов" in describe_item(Client("Иванов"))
    assert "Петров" in describe_item(Agent("Петров", 5))
