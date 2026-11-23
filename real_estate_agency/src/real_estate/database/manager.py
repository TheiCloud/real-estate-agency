"""
Управление базой данных SQLite.

Класс DatabaseManager открывает соединение, создаёт таблицы,
выполняет запросы и закрывает соединение. Реализует
контекстный менеджер (глава 33), поэтому работает с with.
"""

import json
import sqlite3
from pathlib import Path
from types import TracebackType
from typing import Any

from ..exceptions import DatabaseError


class DatabaseManager:
    """
    Управление соединением с базой данных.

    Открывает соединение, создаёт таблицы, выполняет запросы.
    Используется как контекстный менеджер:

        with DatabaseManager("agency.db") as db:
            db.save_apartment(flat)
    """

    def __init__(self, db_path: str | Path = "data/agency.db") -> None:
        """Сохраняет путь к базе до открытия соединения."""
        self.db_path = db_path
        self._connection: sqlite3.Connection | None = None

    def connect(self) -> None:
        """Открывает соединение с базой данных."""
        try:
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            self._connection = sqlite3.connect(self.db_path)
            self._connection.row_factory = sqlite3.Row
            self._connection.execute("PRAGMA foreign_keys = ON")
        except sqlite3.Error as e:
            raise DatabaseError(f"Не удалось открыть БД: {e}")

    def close(self) -> None:
        """Закрывает соединение."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def create_tables(self) -> None:
        """Создаёт таблицы из SQL-схемы."""
        schema_path = Path(__file__).parent / "schema.sql"
        with open(schema_path, encoding="utf-8") as f:
            schema = f.read()

        try:
            self._connection.executescript(schema)
            columns = {
                row["name"]
                for row in self._connection.execute(
                    "PRAGMA table_info(apartments)"
                )
            }
            if "is_rented" not in columns:
                self._connection.execute(
                    "ALTER TABLE apartments ADD COLUMN is_rented "
                    "INTEGER NOT NULL DEFAULT 0"
                )
            if "payload" not in columns:
                self._connection.execute(
                    "ALTER TABLE apartments ADD COLUMN payload TEXT "
                    "NOT NULL DEFAULT '{}'"
                )
            self._connection.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"Не удалось создать таблицы: {e}")

    def save_apartment(self, apartment: Any) -> int:
        """
        Сохраняет объект недвижимости.

        Возвращает id записи. Если адрес уже есть,
        обновляет существующую запись.
        """
        data = apartment.to_dict()
        payload = json.dumps(data, ensure_ascii=False)
        try:
            self._connection.execute(
                """
                INSERT INTO apartments
                    (address, area, price, is_sold, is_rented, type, payload)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(address) DO UPDATE SET
                    area = excluded.area,
                    price = excluded.price,
                    is_sold = excluded.is_sold,
                    is_rented = excluded.is_rented,
                    type = excluded.type,
                    payload = excluded.payload
                """,
                (
                    data["address"],
                    data["area"],
                    data.get("price", 0),
                    int(data.get("is_sold", False)),
                    int(data.get("is_rented", False)),
                    data["type"],
                    payload,
                ),
            )
            self._connection.commit()
            row = self._connection.execute(
                "SELECT id FROM apartments WHERE address = ?",
                (data["address"],),
            ).fetchone()
            return int(row["id"])
        except sqlite3.Error as e:
            raise DatabaseError(f"Не удалось сохранить квартиру: {e}")

    def find_apartment(self, address: str) -> sqlite3.Row | None:
        """Находит квартиру по адресу. Возвращает строку или None."""
        try:
            cursor = self._connection.execute(
                "SELECT * FROM apartments WHERE address = ?",
                (address,),
            )
            return cursor.fetchone()
        except sqlite3.Error as e:
            raise DatabaseError(f"Ошибка поиска: {e}")

    def find_all_apartments(self) -> list[sqlite3.Row]:
        """Возвращает все квартиры."""
        try:
            cursor = self._connection.execute("SELECT * FROM apartments")
            return cursor.fetchall()
        except sqlite3.Error as e:
            raise DatabaseError(f"Ошибка чтения: {e}")

    def delete_apartment(self, address: str) -> bool:
        """Удаляет квартиру по адресу. Возвращает True, если удалено."""
        try:
            cursor = self._connection.execute(
                "DELETE FROM apartments WHERE address = ?",
                (address,),
            )
            self._connection.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            raise DatabaseError(f"Ошибка удаления: {e}")

    def save_client(self, client: Any) -> int:
        """Сохраняет клиента в базу."""
        try:
            row = self._connection.execute(
                "SELECT id FROM clients WHERE name = ?", (client.name,)
            ).fetchone()
            if row is None:
                cursor = self._connection.execute(
                    "INSERT INTO clients (name, budget) VALUES (?, ?)",
                    (client.name, client.budget),
                )
                client_id = cursor.lastrowid
            else:
                client_id = row["id"]
                self._connection.execute(
                    "UPDATE clients SET budget = ? WHERE id = ?",
                    (client.budget, client_id),
                )
            self._connection.commit()
            return int(client_id)
        except sqlite3.Error as e:
            raise DatabaseError(f"Не удалось сохранить клиента: {e}")

    def find_all_clients(self) -> list[sqlite3.Row]:
        """Возвращает все записи клиентов."""
        try:
            return self._connection.execute(
                "SELECT * FROM clients ORDER BY id"
            ).fetchall()
        except sqlite3.Error as e:
            raise DatabaseError(f"Ошибка чтения клиентов: {e}")

    def save_deal(self, deal: dict[str, Any]) -> int:
        """
        Сохраняет сделку.

        deal — словарь с полями apartment_id, client_id,
        agent_id, commission, date.
        """
        try:
            cursor = self._connection.execute(
                """
                INSERT INTO deals
                    (apartment_id, client_id, agent_id, commission, date)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    deal["apartment_id"],
                    deal.get("client_id"),
                    deal.get("agent_id"),
                    deal.get("commission", 0),
                    deal["date"],
                ),
            )
            self._connection.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            raise DatabaseError(f"Не удалось сохранить сделку: {e}")

    def __enter__(self) -> "DatabaseManager":
        """Открывает соединение при входе в with."""
        self.connect()
        self.create_tables()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        """Закрывает соединение при выходе из with."""
        self.close()
        return False
