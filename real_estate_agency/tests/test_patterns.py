"""
Тесты паттернов проектирования.
"""

import pytest

from real_estate.patterns import (
    EstateFactory,
    SingletonMeta,
    ItemDecorator,
    RenovatedDecorator,
    FurnishedDecorator,
    MortgageDecorator,
    ApartmentAdapter,
)
from real_estate.models import Apartment


# ─── Factory ───

def test_factory_apartment():
    """Фабрика создаёт квартиру."""
    flat = EstateFactory.create(
        "apartment", address="ул. Ленина", area=65, price=8_500_000,
    )
    assert flat.address == "ул. Ленина"
    assert flat.area == 65


def test_factory_house():
    """Фабрика создаёт дом."""
    house = EstateFactory.create(
        "house", address="ул. Садовая", area=200, floors=2,
    )
    assert house.floors == 2


def test_factory_studio():
    """Фабрика создаёт студию."""
    studio = EstateFactory.create(
        "studio", address="ул. Пушкина", area=25, price=4_000_000,
    )
    assert studio.get_info().startswith("Студия")


def test_factory_unknown():
    """Неизвестный тип выбрасывает ValueError."""
    with pytest.raises(ValueError):
        EstateFactory.create("unknown", address="a", area=1, price=1)


def test_factory_list_kinds():
    """list_kinds возвращает список доступных типов."""
    kinds = EstateFactory.list_kinds()
    assert "apartment" in kinds
    assert "house" in kinds


def test_factory_register():
    """Декоратор регистрирует новый тип."""

    @EstateFactory.register("villa_test")
    class Villa(Apartment):
        """Тестовый наследник квартиры для проверки регистрации."""
        pass

    villa = EstateFactory.create(
        "villa_test", address="ул. Приморская", area=300, price=80_000_000,
    )
    assert isinstance(villa, Villa)

    # Убираем после теста, чтобы не влиять на другие.
    EstateFactory._registry.pop("villa_test", None)


# ─── Singleton ───

def test_singleton_same_object():
    """Повторное создание возвращает тот же объект."""

    class Registry(metaclass=SingletonMeta):
        """Тестовый реестр для проверки SingletonMeta."""
        def __init__(self):
            """Создаёт список элементов реестра."""
            self.items = []

    r1 = Registry()
    r2 = Registry()
    assert r1 is r2


def test_singleton_state_shared():
    """Состояние общего объекта видно через оба экземпляра."""

    class Registry(metaclass=SingletonMeta):
        """Тестовый реестр для проверки общего состояния."""
        def __init__(self):
            """Создаёт список элементов реестра."""
            self.items = []

    r1 = Registry()
    r1.items.append("a")
    r2 = Registry()
    assert r2.items == ["a"]


def test_singleton_different_classes():
    """Разные классы — разные синглтоны."""

    class A(metaclass=SingletonMeta):
        """Первый независимый singleton-класс."""
        pass

    class B(metaclass=SingletonMeta):
        """Второй независимый singleton-класс."""
        pass

    assert A() is not B()


# ─── Decorator ───

def test_decorator_one(sample_apartment):
    """Один декоратор добавляет метку."""
    decorated = RenovatedDecorator(sample_apartment)
    info = decorated.get_info()
    assert "с ремонтом" in info
    assert sample_apartment.get_info() in info


def test_decorator_two(sample_apartment):
    """Два декоратора складывают метки."""
    decorated = RenovatedDecorator(FurnishedDecorator(sample_apartment))
    info = decorated.get_info()
    assert "с ремонтом" in info
    assert "с мебелью" in info


def test_decorator_three(sample_apartment):
    """Три декоратора складывают метки."""
    decorated = RenovatedDecorator(
        FurnishedDecorator(MortgageDecorator(sample_apartment))
    )
    info = decorated.get_info()
    assert "ипотека возможна" in info
    assert "с мебелью" in info
    assert "с ремонтом" in info


def test_decorator_order(sample_apartment):
    """Порядок декораторов меняет порядок меток."""
    a = RenovatedDecorator(FurnishedDecorator(sample_apartment)).get_info()
    b = FurnishedDecorator(RenovatedDecorator(sample_apartment)).get_info()
    assert a != b


# ─── Adapter ───

def test_adapter_address():
    """Адаптер читает адрес из location."""
    adapter = ApartmentAdapter({
        "location": "ул. Ленина",
        "size": 65,
        "cost": 8_500_000,
    })
    assert adapter.address == "ул. Ленина"


def test_adapter_all_fields():
    """Адаптер читает все поля."""
    adapter = ApartmentAdapter({
        "location": "ул. Садовая",
        "size": 80,
        "cost": 12_000_000,
    })
    assert adapter.area == 80
    assert adapter.price == 12_000_000


def test_adapter_alternate_keys():
    """Адаптер поддерживает и внутренние ключи."""
    adapter = ApartmentAdapter({
        "address": "ул. Мира",
        "area": 55,
        "price": 6_000_000,
    })
    assert adapter.address == "ул. Мира"


def test_adapter_get_info():
    """Адаптер возвращает описание в формате Apartment."""
    adapter = ApartmentAdapter({
        "location": "ул. Ленина",
        "size": 65,
        "cost": 8_500_000,
    })
    assert "ул. Ленина" in adapter.get_info()
    assert "65" in adapter.get_info()
