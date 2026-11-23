"""
Парсер аргументов командной строки.

Создаёт объект ArgumentParser с подкомандами.
Каждая подкоманда — отдельная операция агентства.
"""

import argparse


def create_parser() -> argparse.ArgumentParser:
    """
    Создаёт парсер аргументов с девятью подкомандами.

    Возвращает объект ArgumentParser, готовый к разбору
    аргументов из sys.argv.
    """
    parser = argparse.ArgumentParser(
        prog="agency",
        description="Система учёта агентства недвижимости",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help="Доступные команды",
    )

    # ─── add ───
    add_parser = subparsers.add_parser(
        "add",
        help="Добавить объект недвижимости",
    )
    add_parser.add_argument(
        "--address", required=True, help="Адрес объекта",
    )
    add_parser.add_argument(
        "--area", type=int, required=True, help="Площадь в м²",
    )
    add_parser.add_argument(
        "--price", type=int, required=True, help="Цена",
    )
    add_parser.add_argument(
        "--floors", type=int, help="Количество этажей (для дома)",
    )
    add_parser.add_argument(
        "--type",
        default="apartment",
        choices=["apartment", "studio", "two_room", "house", "penthouse"],
        help="Тип объекта",
    )

    # ─── list ───
    subparsers.add_parser("list", help="Показать все объекты")

    # ─── find ───
    find_parser = subparsers.add_parser(
        "find",
        help="Найти объект по адресу",
    )
    find_parser.add_argument(
        "--address", required=True, help="Адрес объекта",
    )

    # ─── sell ───
    sell_parser = subparsers.add_parser(
        "sell",
        help="Продать объект",
    )
    sell_parser.add_argument(
        "--address", required=True, help="Адрес объекта",
    )
    sell_parser.add_argument(
        "--buyer", required=True, help="Имя покупателя",
    )

    # ─── rent ───
    rent_parser = subparsers.add_parser(
        "rent",
        help="Сдать объект в аренду",
    )
    rent_parser.add_argument(
        "--address", required=True, help="Адрес объекта",
    )
    rent_parser.add_argument(
        "--tenant", required=True, help="Имя арендатора",
    )
    rent_parser.add_argument(
        "--days", type=int, required=True, help="Срок аренды в днях",
    )

    # ─── subscribe ───
    subscribe_parser = subparsers.add_parser(
        "subscribe",
        help="Подписать клиента на уведомления",
    )
    subscribe_parser.add_argument(
        "--name", required=True, help="Имя клиента",
    )
    subscribe_parser.add_argument(
        "--budget", type=int, default=0, help="Бюджет клиента",
    )

    # ─── report ───
    subparsers.add_parser("report", help="Сгенерировать отчёт")

    # ─── save ───
    subparsers.add_parser("save", help="Сохранить в БД")

    # ─── load ───
    subparsers.add_parser("load", help="Загрузить из БД")

    return parser
