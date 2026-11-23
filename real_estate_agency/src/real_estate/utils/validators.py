"""
Статические утилиты для проверки данных.

Класс не имеет состояния. Все методы — статические.
Вызываются напрямую через имя класса:

    EstateUtils.is_valid_area(65)
"""


class EstateUtils:
    """
    Утилиты для проверки корректности данных о недвижимости.

    Все методы — статические. Объект класса создавать не нужно.
    """

    @staticmethod
    def is_valid_area(area: object) -> bool:
        """
        Проверяет, является ли площадь корректной.

        Площадь должна быть числом в диапазоне от 5 до 500 м².
        """
        return (
            isinstance(area, (int, float))
            and not isinstance(area, bool)
            and 5 <= area <= 500
        )

    @staticmethod
    def is_valid_price(price: object) -> bool:
        """
        Проверяет, является ли цена корректной.

        Цена должна быть положительным числом.
        """
        return (
            isinstance(price, (int, float))
            and not isinstance(price, bool)
            and price > 0
        )

    @staticmethod
    def is_valid_address(address: object) -> bool:
        """
        Проверяет, является ли адрес корректным.

        Адрес должен быть непустой строкой.
        """
        return isinstance(address, str) and len(address.strip()) > 0
