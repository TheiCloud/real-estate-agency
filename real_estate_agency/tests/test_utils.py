"""Тесты интерфейсов, исключений и утилит проекта."""

import logging

import pytest

from real_estate.exceptions import (
    AgencyError,
    ApartmentNotFoundError,
    InvalidAreaError,
)
from real_estate.interfaces import (
    Infoable,
    Notifier,
    LoggableMixin,
    Rentable,
    Renovatable,
    Sellable,
    Storage,
    TimestampMixin,
)
from real_estate.models import Building
from real_estate.services import EstateStorage
from real_estate.utils import (
    AgencyLogger,
    EstateUtils,
    RangeDescriptor,
    setup_logging,
)


class BoundedValue:
    """Пример класса, проверяющего атрибут дескриптором."""

    value = RangeDescriptor(1, 10)


def test_range_descriptor_accepts_values_in_range():
    """Дескриптор сохраняет допустимые числовые значения."""
    item = BoundedValue()
    item.value = 5
    assert item.value == 5


@pytest.mark.parametrize("value", [0, 11])
def test_range_descriptor_rejects_values_outside_range(value):
    """Дескриптор отклоняет значения за границами."""
    with pytest.raises(ValueError):
        BoundedValue().value = value


@pytest.mark.parametrize("value", ["5", True, None])
def test_range_descriptor_rejects_non_numeric_values(value):
    """Дескриптор требует число и не принимает bool."""
    with pytest.raises(TypeError):
        BoundedValue().value = value


@pytest.mark.parametrize("area", [5, 65, 500, 25.5])
def test_estate_utils_accepts_valid_area(area):
    """Площадь проходит проверку в допустимом диапазоне."""
    assert EstateUtils.is_valid_area(area)


@pytest.mark.parametrize("area", [4, 501, True, "65"])
def test_estate_utils_rejects_invalid_area(area):
    """Площадь вне диапазона или неверного типа отклоняется."""
    assert not EstateUtils.is_valid_area(area)


def test_estate_utils_validates_price_and_address():
    """Статические методы проверяют цену и адрес."""
    assert EstateUtils.is_valid_price(1)
    assert not EstateUtils.is_valid_price(0)
    assert not EstateUtils.is_valid_price(True)
    assert EstateUtils.is_valid_address("ул. Ленина")
    assert not EstateUtils.is_valid_address("  ")
    assert not EstateUtils.is_valid_address(None)


def test_range_descriptor_is_class_accessible():
    """При обращении через класс возвращается сам дескриптор."""
    assert isinstance(BoundedValue.value, RangeDescriptor)
    assert BoundedValue().value is None


def test_invalid_area_error_classifies_range():
    """Исключение сообщает, в какую сторону нарушена граница."""
    assert InvalidAreaError(2).is_too_small()
    assert not InvalidAreaError(2).is_too_large()
    assert InvalidAreaError(600).is_too_large()
    assert not InvalidAreaError(600).is_too_small()


def test_domain_errors_inherit_from_agency_error():
    """Собственные ошибки можно перехватывать общим классом."""
    error = ApartmentNotFoundError("ул. Ленина")
    assert isinstance(error, AgencyError)
    assert error.address == "ул. Ленина"


@pytest.mark.parametrize(
    "interface",
    [Infoable, Notifier, Rentable, Renovatable, Sellable, Storage],
)
def test_abstract_interfaces_cannot_be_instantiated(interface):
    """ABC интерфейсы запрещают создавать неполные реализации."""
    with pytest.raises(TypeError):
        interface()


def test_estate_storage_implements_storage_contract():
    """Хранилище реализует абстрактный контракт Storage."""
    storage = EstateStorage()
    storage.save(object())
    assert len(storage) == 1


def test_loggable_mixin_writes_timestamp_and_class(capsys):
    """Миксин добавляет имя класса и временную метку."""

    class Logged(LoggableMixin, TimestampMixin):
        """Класс с логированием и временем создания."""

    item = Logged()
    item.log("готово")
    assert "Logged" in capsys.readouterr().out


def test_timestamp_mixin_sets_datetime():
    """TimestampMixin сохраняет момент создания объекта."""
    class Timed(TimestampMixin):
        """Объект для проверки временной метки."""

    item = Timed()
    item.set_created()
    assert item.created_at is not None


def test_building_uses_slots():
    """Building хранит только объявленные поля через slots."""
    building = Building("Дом", 5)
    assert not hasattr(building, "__dict__")
    with pytest.raises(AttributeError):
        building.extra = "поле"


def test_setup_logging_does_not_add_duplicate_handlers():
    """Повторная настройка возвращает логгер без дублей."""
    logger = logging.getLogger("real_estate")
    original_handlers = list(logger.handlers)
    logger.handlers.clear()
    try:
        first = setup_logging(logging.WARNING)
        count = len(first.handlers)
        second = setup_logging(logging.INFO)
        assert first is second
        assert len(second.handlers) == count == 1
        assert second.level == logging.INFO
    finally:
        logger.handlers.clear()
        logger.handlers.extend(original_handlers)


def test_agency_logger_logs_at_requested_level(caplog):
    """Обёртка пишет сообщение в стандартный logging."""
    logger = logging.getLogger("real_estate.test")
    logger.setLevel(logging.INFO)
    with caplog.at_level(logging.INFO, logger="real_estate.test"):
        AgencyLogger("test").info("сообщение")
    assert "сообщение" in caplog.text
