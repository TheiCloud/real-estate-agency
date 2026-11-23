"""
Собственные исключения проекта.

Все исключения наследуются от AgencyError. Это позволяет
ловить как конкретную ошибку, так и все ошибки агентства сразу.
"""


class AgencyError(Exception):
    """
    Базовое исключение агентства.

    Все остальные ошибки проекта наследуются от него.
    Ловить AgencyError — значит ловить все свои ошибки.
    """
    pass


class ApartmentNotFoundError(AgencyError):
    """Квартира по указанному адресу не найдена."""

    def __init__(self, address: str) -> None:
        """Сохраняет адрес, по которому объект не найден."""
        self.address = address
        super().__init__(f"Объект по адресу {address!r} не найден")


class ApartmentAlreadySoldError(AgencyError):
    """Объект недвижимости уже продан."""

    def __init__(self, address: str) -> None:
        """Сохраняет адрес уже проданного объекта."""
        self.address = address
        super().__init__(f"Объект {address!r} уже продан")


class ItemNotSellableError(AgencyError):
    """Объект нельзя продать."""


class PropertyAlreadyExistsError(AgencyError):
    """В хранилище уже есть объект с таким адресом."""

    def __init__(self, address: str) -> None:
        """Сохраняет повторяющийся адрес."""
        self.address = address
        super().__init__(f"Объект по адресу {address!r} уже существует")


class ItemNotRentableError(AgencyError):
    """Объект нельзя сдать в аренду."""


class ItemAlreadyRentedError(AgencyError):
    """Объект уже находится в аренде."""


class ItemNotRentedError(AgencyError):
    """Объект не находится в аренде."""


class InvalidRentalPeriodError(AgencyError):
    """Срок аренды должен быть положительным целым числом дней."""


class InvalidAreaError(AgencyError):
    """Некорректная площадь — вне допустимого диапазона."""

    def __init__(
        self,
        area: int | float,
        min_area: int | float = 5,
        max_area: int | float = 500,
    ) -> None:
        """Сохраняет площадь и границы допустимого диапазона."""
        self.area = area
        self.min_area = min_area
        self.max_area = max_area
        super().__init__(
            f"Площадь {area} м² вне диапазона [{min_area}, {max_area}]"
        )

    def is_too_small(self) -> bool:
        """Проверяет, меньше ли площадь минимальной."""
        return self.area < self.min_area

    def is_too_large(self) -> bool:
        """Проверяет, больше ли площадь максимальной."""
        return self.area > self.max_area


class DatabaseError(AgencyError):
    """Ошибка при работе с базой данных."""

    def __init__(self, message: str) -> None:
        """Сохраняет исходное сообщение ошибки базы данных."""
        self.message = message
        super().__init__(f"Ошибка БД: {message}")
