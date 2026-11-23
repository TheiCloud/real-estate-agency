"""
Сервис отчётов.

Отвечает только за формирование отчётов (SRP, глава 27).
Не хранит данные, не оформляет сделки — только генерирует текст.
"""


from typing import Any


class ReportService:
    """
    Формирует отчёты о работе агентства.

    Первый метод — отчёт по всем объектам хранилища.
    Второй метод — отчёт по проданным объектам.
    """

    def generate(self, storage: Any, agency_name: str) -> str:
        """
        Формирует общий отчёт по всем объектам.

        Возвращает многострочную строку: название агентства,
        список объектов с их статусом.
        """
        lines = [f"Агентство: {agency_name}"]

        for item in storage.list_all():
            status = (
                "продана"
                if getattr(item, "is_sold", False)
                else "в продаже"
            )
            lines.append(f"  - {item.get_info()} [{status}]")

        return "\n".join(lines)

    def generate_sales_report(self, deals: list[dict[str, Any]]) -> str:
        """
        Формирует отчёт по сделкам.

        Показывает количество сделок и суммарную комиссию.
        """
        if not deals:
            return "Сделок не было"

        total_commission = sum(deal["commission"] for deal in deals)
        count = len(deals)

        lines = [
            f"Всего сделок: {count}",
            f"Суммарная комиссия: {total_commission:,.0f} ₽".replace(",", " "),
        ]

        for i, deal in enumerate(deals, start=1):
            address = deal["item"].address
            buyer = deal["buyer"]
            commission = deal["commission"]
            lines.append(
                f"  {i}. {address} → {buyer} "
                f"(комиссия: {commission:,.0f} ₽)".replace(",", " ")
            )

        return "\n".join(lines)
