"""
Тесты сервисов.

Проверяют хранение, сделки, уведомления, отчёты, стратегии.
"""

import pytest

from real_estate.models import Apartment, Client
from real_estate.services import (
    EstateStorage,
    DealService,
    RentalService,
    NotificationService,
    ReportService,
    EmailNotifier,
    SmsNotifier,
    FixedCommission,
    PercentCommission,
    LoyaltyCommission,
    CommissionCalculator,
)
from real_estate.exceptions import (
    ApartmentNotFoundError,
    ApartmentAlreadySoldError,
    InvalidRentalPeriodError,
    ItemAlreadyRentedError,
    ItemNotRentedError,
    ItemNotRentableError,
    ItemNotSellableError,
    PropertyAlreadyExistsError,
)


# ─── EstateStorage ───

def test_storage_add_and_len(sample_apartment, sample_storage):
    """Объект добавляется, длина растёт."""
    sample_storage.add(sample_apartment)
    assert len(sample_storage) == 1


def test_storage_rejects_duplicate_address(sample_apartment, sample_storage):
    """Хранилище запрещает несколько записей с одним адресом."""
    sample_storage.add(sample_apartment)
    with pytest.raises(PropertyAlreadyExistsError):
        sample_storage.add(Apartment(sample_apartment.address, 70, 9_000_000))


def test_storage_find(sample_apartment, sample_storage):
    """Поиск возвращает добавленный объект."""
    sample_storage.add(sample_apartment)
    found = sample_storage.find_by_address("ул. Ленина, д. 10, кв. 5")
    assert found is sample_apartment


def test_storage_find_not_found(sample_storage):
    """Поиск несуществующего выбрасывает ApartmentNotFoundError."""
    with pytest.raises(ApartmentNotFoundError):
        sample_storage.find_by_address("несуществующий")


def test_storage_contains(sample_apartment, sample_storage):
    """Оператор in работает."""
    sample_storage.add(sample_apartment)
    assert sample_apartment in sample_storage


def test_storage_getitem(sample_apartment, sample_storage):
    """Доступ по индексу работает."""
    sample_storage.add(sample_apartment)
    assert sample_storage[0] is sample_apartment


def test_storage_iter(sample_apartment, sample_house, sample_storage):
    """Итерация работает и повторяется."""
    sample_storage.add(sample_apartment)
    sample_storage.add(sample_house)

    first = list(sample_storage)
    second = list(sample_storage)

    assert len(first) == 2
    assert len(second) == 2


def test_storage_remove_clear_and_copy(sample_apartment, sample_storage):
    """Удаление, очистка и list_all не раскрывают внутренний список."""
    sample_storage.add(sample_apartment)
    listed = sample_storage.list_all()
    listed.clear()
    assert len(sample_storage) == 1
    sample_storage.remove(sample_apartment)
    assert len(sample_storage) == 0
    sample_storage.add(sample_apartment)
    sample_storage.clear()
    assert len(sample_storage) == 0


# ─── NotificationService ───

def test_notification_subscribe():
    """Подписка увеличивает счётчик."""
    service = NotificationService()
    client = Client("Иванов")
    service.subscribe(client)
    assert service.count() == 1


def test_notification_no_duplicates():
    """Повторная подписка не дублирует."""
    service = NotificationService()
    client = Client("Иванов")
    service.subscribe(client)
    service.subscribe(client)
    assert service.count() == 1


def test_notification_unsubscribe():
    """Отписка уменьшает счётчик."""
    service = NotificationService()
    client = Client("Иванов")
    service.subscribe(client)
    service.unsubscribe(client)
    assert service.count() == 0


def test_notification_notify():
    """Уведомление доходит до клиента."""
    service = NotificationService()
    client = Client("Иванов")
    service.subscribe(client)
    service.notify("Событие")
    assert len(client.notifications) == 1


def test_notification_after_unsubscribe():
    """После отписки клиент не получает уведомлений."""
    service = NotificationService()
    client = Client("Иванов")
    service.subscribe(client)
    service.unsubscribe(client)
    service.notify("Событие")
    assert len(client.notifications) == 0


def test_notification_clear():
    """Очистка удаляет всех подписчиков."""
    service = NotificationService()
    service.subscribe(Client("Иванов"))
    service.clear()
    assert service.count() == 0


# ─── Commission ───

def test_fixed_commission():
    """Фиксированная комиссия не зависит от цены."""
    strategy = FixedCommission(amount=50_000)
    assert strategy.calculate(1_000_000) == 50_000
    assert strategy.calculate(10_000_000) == 50_000


def test_percent_commission():
    """Процентная комиссия зависит от цены."""
    strategy = PercentCommission(rate=0.03)
    assert strategy.calculate(1_000_000) == 30_000


def test_loyalty_commission():
    """Льготная комиссия использует ставку 1.5%."""
    strategy = LoyaltyCommission()
    assert strategy.calculate(1_000_000) == 15_000


def test_commission_calculator_is_callable_and_accepts_strategy_class():
    """Калькулятор делегирует расчёт переданной стратегии."""
    calculator = CommissionCalculator(PercentCommission)
    assert calculator(1_000_000) == 30_000


@pytest.mark.parametrize(
    "strategy",
    [lambda: FixedCommission(amount=-1), lambda: PercentCommission(rate=1.1)],
)
def test_commission_strategies_validate_configuration(strategy):
    """Стратегии отклоняют некорректные настройки."""
    with pytest.raises(ValueError):
        strategy()


def test_commission_calculator_requires_strategy():
    """Калькулятор принимает только CommissionStrategy."""
    with pytest.raises(TypeError):
        CommissionCalculator(object())


# ─── DealService ───

def test_deal_sell(sample_apartment, sample_storage):
    """Продажа помечает квартиру и возвращает результат."""
    sample_storage.add(sample_apartment)
    service = DealService(
        sample_storage, EmailNotifier(), PercentCommission()
    )
    result = service.sell("ул. Ленина, д. 10, кв. 5", "Петров")

    assert sample_apartment.is_sold is True
    assert result["buyer"] == "Петров"
    assert result["commission"] == 8_500_000 * 0.03


def test_deal_sell_not_found(sample_storage):
    """Продажа несуществующей квартиры выбрасывает исключение."""
    service = DealService(sample_storage, EmailNotifier())
    with pytest.raises(ApartmentNotFoundError):
        service.sell("несуществующий", "Петров")


def test_deal_sell_twice(sample_apartment, sample_storage):
    """Продажа уже проданной выбрасывает ApartmentAlreadySoldError."""
    sample_storage.add(sample_apartment)
    service = DealService(sample_storage, EmailNotifier())
    service.sell("ул. Ленина, д. 10, кв. 5", "Петров")
    with pytest.raises(ApartmentAlreadySoldError):
        service.sell("ул. Ленина, д. 10, кв. 5", "Сидоров")


def test_deal_sell_without_commission(sample_apartment, sample_storage):
    """Если стратегия не задана, комиссия равна нулю."""
    sample_storage.add(sample_apartment)
    service = DealService(sample_storage, EmailNotifier())
    result = service.sell("ул. Ленина, д. 10, кв. 5", "Петров")
    assert result["commission"] == 0


def test_deal_rejects_non_sellable_item(sample_storage):
    """Сервис не продаёт объект без контракта Sellable."""
    class ReadOnlyItem:
        """Минимальный объект без возможности продажи."""
        address = "Адрес"

        def get_info(self):
            """Возвращает краткое описание для поиска."""
            return "Описание"

    sample_storage.add(ReadOnlyItem())
    with pytest.raises(ItemNotSellableError):
        DealService(sample_storage, EmailNotifier()).sell("Адрес", "Иванов")


# ─── RentalService ───

def test_rental_rent(sample_apartment, sample_storage):
    """Аренда помечает объект и возвращает результат."""
    sample_storage.add(sample_apartment)
    service = RentalService(sample_storage, EmailNotifier())
    result = service.rent("ул. Ленина, д. 10, кв. 5", "Иванов", 30)

    assert result["tenant"] == "Иванов"
    assert result["days"] == 30
    assert sample_apartment.is_rented is True


def test_rental_return(sample_apartment, sample_storage):
    """Возврат из аренды снимает флаг."""
    sample_storage.add(sample_apartment)
    service = RentalService(sample_storage, EmailNotifier())
    service.rent("ул. Ленина, д. 10, кв. 5", "Иванов", 30)
    service.return_item("ул. Ленина, д. 10, кв. 5")
    assert sample_apartment.is_rented is False


def test_rental_rejects_invalid_period(sample_apartment, sample_storage):
    """Срок аренды должен быть положительным целым числом."""
    sample_storage.add(sample_apartment)
    service = RentalService(sample_storage, EmailNotifier())
    with pytest.raises(InvalidRentalPeriodError):
        service.rent(sample_apartment.address, "Иванов", 0)


def test_rental_rejects_already_rented_item(sample_apartment, sample_storage):
    """Нельзя сдать объект повторно до его возврата."""
    sample_storage.add(sample_apartment)
    service = RentalService(sample_storage, EmailNotifier())
    service.rent(sample_apartment.address, "Иванов", 30)
    with pytest.raises(ItemAlreadyRentedError):
        service.rent(sample_apartment.address, "Петров", 10)


def test_rental_requires_rentable_item(sample_house, sample_storage):
    """Дом нельзя сдать, если он не реализует Rentable."""
    sample_storage.add(sample_house)
    with pytest.raises(ItemNotRentableError):
        RentalService(sample_storage, EmailNotifier()).rent(
            sample_house.address, "Иванов", 30
        )


def test_rental_return_requires_active_rental(
    sample_apartment,
    sample_storage,
):
    """Возврат возможен только для объекта в активной аренде."""
    sample_storage.add(sample_apartment)
    with pytest.raises(ItemNotRentedError):
        RentalService(sample_storage, EmailNotifier()).return_item(
            sample_apartment.address
        )


# ─── ReportService ───

def test_report_generate(sample_apartment, sample_storage):
    """Отчёт содержит адрес и название агентства."""
    sample_storage.add(sample_apartment)
    reports = ReportService()
    text = reports.generate(sample_storage, "Дом-Сервис")
    assert "Дом-Сервис" in text
    assert "ул. Ленина" in text


def test_report_sales_empty():
    """Пустой отчёт по сделкам — сообщение об отсутствии."""
    reports = ReportService()
    text = reports.generate_sales_report([])
    assert "не было" in text.lower()


def test_report_sales_with_deals(sample_apartment, sample_storage):
    """Отчёт по сделкам содержит количество и комиссию."""
    sample_storage.add(sample_apartment)
    service = DealService(
        sample_storage, EmailNotifier(), PercentCommission()
    )
    deal = service.sell("ул. Ленина, д. 10, кв. 5", "Петров")

    reports = ReportService()
    text = reports.generate_sales_report([deal])
    assert "1" in text
    assert "255" in text


# ─── Notifier ───

def test_email_notifier(capsys):
    """EmailNotifier печатает сообщение с префиксом."""
    notifier = EmailNotifier()
    notifier.send("Привет")
    captured = capsys.readouterr()
    assert "[Email]" in captured.out
    assert "Привет" in captured.out


def test_sms_notifier(capsys):
    """SmsNotifier печатает сообщение с префиксом."""
    notifier = SmsNotifier()
    notifier.send("Привет")
    captured = capsys.readouterr()
    assert "[SMS]" in captured.out
