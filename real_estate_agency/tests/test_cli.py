"""
Тесты CLI: парсер и команды.
"""

import pytest

from real_estate.cli import create_parser, Commands


# ─── Парсер ───

def test_parser_creates():
    """Парсер создаётся."""
    parser = create_parser()
    assert parser is not None


def test_parser_add_command():
    """Парсер разбирает команду add."""
    parser = create_parser()
    args = parser.parse_args([
        "add",
        "--address", "ул. Ленина",
        "--area", "65",
        "--price", "8500000",
    ])
    assert args.command == "add"
    assert args.address == "ул. Ленина"
    assert args.area == 65
    assert args.price == 8_500_000
    assert args.type == "apartment"


def test_parser_add_with_type():
    """Парсер принимает тип."""
    parser = create_parser()
    args = parser.parse_args([
        "add",
        "--address", "ул. Ленина",
        "--area", "65",
        "--price", "8500000",
        "--type", "studio",
    ])
    assert args.type == "studio"


def test_parser_house_accepts_floors():
    """Парсер принимает число этажей для дома."""
    args = create_parser().parse_args([
        "add",
        "--address", "ул. Садовая",
        "--area", "200",
        "--price", "18000000",
        "--type", "house",
        "--floors", "2",
    ])
    assert args.type == "house"
    assert args.floors == 2


def test_parser_sell_command():
    """Парсер разбирает команду sell."""
    parser = create_parser()
    args = parser.parse_args([
        "sell",
        "--address", "ул. Ленина",
        "--buyer", "Петров",
    ])
    assert args.command == "sell"
    assert args.buyer == "Петров"


def test_parser_rent_command():
    """Парсер разбирает команду rent."""
    parser = create_parser()
    args = parser.parse_args([
        "rent",
        "--address", "ул. Ленина",
        "--tenant", "Иванов",
        "--days", "30",
    ])
    assert args.days == 30


def test_parser_invalid_type():
    """Неизвестный тип вызывает SystemExit."""
    parser = create_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([
            "add",
            "--address", "a",
            "--area", "65",
            "--price", "1000",
            "--type", "unknown",
        ])


# ─── Команды ───

class FakeArgs:
    """Фиктивный объект аргументов для тестов."""
    def __init__(self, **kwargs):
        """Копирует переданные значения в атрибуты."""
        for key, value in kwargs.items():
            setattr(self, key, value)


def test_cmd_add(capsys):
    """cmd_add добавляет квартиру и печатает сообщение."""
    commands = Commands()
    commands.cmd_add(FakeArgs(
        type="apartment",
        address="ул. Ленина",
        area=65,
        price=8_500_000,
    ))
    captured = capsys.readouterr()
    assert "Добавлено" in captured.out
    assert len(commands.storage) == 1


def test_cmd_list_empty(capsys):
    """cmd_list на пустом хранилище печатает сообщение."""
    commands = Commands()
    commands.cmd_list(FakeArgs())
    captured = capsys.readouterr()
    assert "пусто" in captured.out.lower()


def test_cmd_list_with_items(capsys):
    """cmd_list показывает объекты."""
    commands = Commands()
    commands.cmd_add(FakeArgs(
        type="apartment",
        address="ул. Ленина",
        area=65,
        price=8_500_000,
    ))
    capsys.readouterr()

    commands.cmd_list(FakeArgs())
    captured = capsys.readouterr()
    assert "ул. Ленина" in captured.out


def test_cmd_find(capsys):
    """cmd_find находит квартиру."""
    commands = Commands()
    commands.cmd_add(FakeArgs(
        type="apartment",
        address="ул. Ленина",
        area=65,
        price=8_500_000,
    ))
    capsys.readouterr()

    commands.cmd_find(FakeArgs(address="ул. Ленина"))
    captured = capsys.readouterr()
    assert "Найдено" in captured.out


def test_cmd_find_not_found(capsys):
    """cmd_find на несуществующем показывает ошибку."""
    commands = Commands()
    commands.cmd_find(FakeArgs(address="несуществующий"))
    captured = capsys.readouterr()
    assert "Ошибка" in captured.out


def test_cmd_sell(capsys):
    """cmd_sell продаёт квартиру."""
    commands = Commands()
    commands.cmd_add(FakeArgs(
        type="apartment",
        address="ул. Ленина",
        area=65,
        price=8_500_000,
    ))
    capsys.readouterr()

    commands.cmd_sell(FakeArgs(address="ул. Ленина", buyer="Петров"))
    captured = capsys.readouterr()
    assert "Продано" in captured.out
    assert "Комиссия" in captured.out


def test_cmd_subscribe(capsys):
    """cmd_subscribe подписывает клиента."""
    commands = Commands()
    commands.cmd_subscribe(FakeArgs(name="Иванов", budget=10_000_000))
    captured = capsys.readouterr()
    assert "Подписан" in captured.out
    assert commands.notifier.count() == 1


def test_cmd_report(capsys):
    """cmd_report печатает отчёт."""
    commands = Commands()
    commands.cmd_report(FakeArgs())
    captured = capsys.readouterr()
    assert "Агентство" in captured.out


def test_cmd_save_and_load(capsys, tmp_path):
    """cmd_save сохраняет, cmd_load загружает."""
    commands = Commands()
    commands.db_path = str(tmp_path / "cli_test.db")

    commands.cmd_add(FakeArgs(
        type="apartment",
        address="ул. Ленина",
        area=65,
        price=8_500_000,
    ))
    capsys.readouterr()

    commands.cmd_save(FakeArgs())
    captured = capsys.readouterr()
    assert "Сохранено" in captured.out

    commands.storage = commands.storage.__class__()
    commands.cmd_load(FakeArgs())
    captured = capsys.readouterr()
    assert "Загружено" in captured.out


def test_cli_persists_state_between_processes(capsys, tmp_path):
    """CLI загружает объекты и клиентов при новом запуске."""
    db_path = str(tmp_path / "persistent_cli.db")
    first = Commands(db_path=db_path, autosave=True)
    first.cmd_add(FakeArgs(
        type="apartment",
        address="ул. Ленина",
        area=65,
        price=8_500_000,
    ))
    first.cmd_subscribe(FakeArgs(name="Иванов", budget=10_000_000))
    capsys.readouterr()

    second = Commands(db_path=db_path, autoload=True, autosave=True)
    assert len(second.storage) == 1
    assert second.storage[0].address == "ул. Ленина"
    assert second.notifier.count() == 1
    second.cmd_sell(FakeArgs(address="ул. Ленина", buyer="Петров"))
    capsys.readouterr()

    third = Commands(db_path=db_path, autoload=True)
    assert third.storage[0].is_sold is True


def test_cmd_add_house_requires_floors(capsys):
    """Команда сообщает, если у дома не указаны этажи."""
    commands = Commands()
    commands.cmd_add(FakeArgs(
        type="house",
        address="ул. Садовая",
        area=200,
        price=18_000_000,
    ))
    assert "--floors" in capsys.readouterr().out
    assert len(commands.storage) == 0
