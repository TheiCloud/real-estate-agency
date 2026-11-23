"""
Обработчики команд CLI.

Класс Commands связывает команды из парсера с сервисами
проекта. Каждый метод выполняет одну команду.
"""

import argparse
from pathlib import Path

from ..patterns import EstateFactory
from ..services import (
    EstateStorage,
    DealService,
    RentalService,
    NotificationService,
    ReportService,
    EmailNotifier,
    PercentCommission,
)
from ..database import (
    DatabaseManager,
    ApartmentRepository,
    ClientRepository,
)
from ..models import Client
from ..exceptions import AgencyError


class Commands:
    """
    Обработчики команд командной строки.

    Создаёт все сервисы проекта и вызывает их
    в соответствующих методах.
    """

    def __init__(
        self,
        db_path: str | Path = "data/agency.db",
        *,
        autoload: bool = False,
        autosave: bool = False,
        agency_name: str = "Дом-Сервис",
    ) -> None:
        """Создаёт сервисы и настраивает режим хранения CLI."""
        """Создаёт сервисы и настраивает режим хранения CLI."""
        self.storage = EstateStorage()
        self.notifier = NotificationService()
        self.email = EmailNotifier()
        self.reports = ReportService()
        self.deals = DealService(
            self.storage, self.email, PercentCommission()
        )
        self.rentals = RentalService(self.storage, self.email)
        self.clients = []
        self.db_path = db_path
        self.autosave = autosave
        self.agency_name = agency_name
        if autoload:
            self._load_from_db()

    def _get_db(self) -> DatabaseManager:
        """Возвращает контекстный менеджер для работы с БД."""
        return DatabaseManager(self.db_path)

    def _save_to_db(self) -> None:
        """Сохраняет объекты и клиентов в настроенную базу."""
        with self._get_db() as db:
            item_repo = ApartmentRepository(db)
            client_repo = ClientRepository(db)
            for item in self.storage:
                item_repo.save(item)
            for client in self.clients:
                client_repo.save(client)

    def _load_from_db(self) -> None:
        """Загружает объекты и клиентов, не заменяя сервисы."""
        with self._get_db() as db:
            items = ApartmentRepository(db).find_all()
            clients = ClientRepository(db).find_all()
        self.storage.clear()
        self.clients.clear()
        self.notifier.clear()
        for item in items:
            self.storage.add(item)
        for client in clients:
            self.clients.append(client)
            self.notifier.subscribe(client)

    def _autosave(self) -> None:
        """Сохраняет изменения для CLI, работающего между запусками."""
        if self.autosave:
            self._save_to_db()

    # ─── add ───
    def cmd_add(self, args: argparse.Namespace) -> None:
        """Добавляет новый объект недвижимости."""
        try:
            item_kwargs = {
                "address": args.address,
                "area": args.area,
                "price": args.price,
            }
            if args.type == "house":
                floors = getattr(args, "floors", None)
                if floors is None:
                    raise ValueError("Для дома укажите --floors")
                item_kwargs["floors"] = floors
            item = EstateFactory.create(args.type, **item_kwargs)
            self.storage.add(item)
            self._autosave()
            print(f"✓ Добавлено: {item.get_info()}")
        except (AgencyError, ValueError, TypeError) as e:
            print(f"✗ Ошибка: {e}")

    # ─── list ───
    def cmd_list(self, args: argparse.Namespace) -> None:
        """Показывает все объекты в хранилище."""
        if len(self.storage) == 0:
            print("Хранилище пусто")
            return

        print(f"Всего объектов: {len(self.storage)}")
        for i, item in enumerate(self.storage, start=1):
            print(f"  {i}. {item.get_info()}")

    # ─── find ───
    def cmd_find(self, args: argparse.Namespace) -> None:
        """Ищет объект по адресу."""
        try:
            item = self.storage.find_by_address(args.address)
            print(f"Найдено: {item.get_info()}")
        except AgencyError as e:
            print(f"✗ Ошибка: {e}")

    # ─── sell ───
    def cmd_sell(self, args: argparse.Namespace) -> None:
        """Продаёт объект по адресу."""
        try:
            result = self.deals.sell(args.address, args.buyer)
            self._autosave()
            commission = result["commission"]
            print(f"✓ Продано: {args.address} → {args.buyer}")
            print(f"  Комиссия: {commission:,.0f} ₽".replace(",", " "))
        except (AgencyError, TypeError, ValueError) as e:
            print(f"✗ Ошибка: {e}")

    # ─── rent ───
    def cmd_rent(self, args: argparse.Namespace) -> None:
        """Сдаёт объект в аренду."""
        try:
            result = self.rentals.rent(
                args.address, args.tenant, args.days
            )
            self._autosave()
            print(
                f"✓ Сдано: {args.address} → {args.tenant} "
                f"на {result['days']} дней"
            )
        except (AgencyError, TypeError, ValueError) as e:
            print(f"✗ Ошибка: {e}")

    # ─── subscribe ───
    def cmd_subscribe(self, args: argparse.Namespace) -> None:
        """Подписывает клиента на уведомления."""
        client = Client(args.name, args.budget)
        self.notifier.subscribe(client)
        self.clients.append(client)
        try:
            self._autosave()
        except AgencyError as e:
            print(f"✗ Ошибка сохранения клиента: {e}")
        print(f"✓ Подписан: {client.describe()}")
        print(f"  Подписчиков: {self.notifier.count()}")

    # ─── report ───
    def cmd_report(self, args: argparse.Namespace) -> None:
        """Генерирует отчёт по хранилищу."""
        report = self.reports.generate(self.storage, self.agency_name)
        print(report)

    # ─── save ───
    def cmd_save(self, args: argparse.Namespace) -> None:
        """Сохраняет объекты из хранилища в базу."""
        if len(self.storage) == 0 and not self.clients:
            print("Нечего сохранять")
            return

        try:
            count = len(self.storage)
            self._save_to_db()
            print(f"✓ Сохранено объектов: {count}")
        except AgencyError as e:
            print(f"✗ Ошибка: {e}")

    # ─── load ───
    def cmd_load(self, args: argparse.Namespace) -> None:
        """Загружает объекты из базы в хранилище."""
        try:
            self._load_from_db()
            print(f"✓ Загружено объектов: {len(self.storage)}")
        except AgencyError as e:
            print(f"✗ Ошибка: {e}")
