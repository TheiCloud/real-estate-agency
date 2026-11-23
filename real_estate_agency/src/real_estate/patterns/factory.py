"""
Фабрика объектов недвижимости.

Паттерн Factory (глава 25). Скрывает логику создания
объектов за единым интерфейсом. Добавление нового типа
не требует изменения существующего кода (OCP, глава 35).
"""

from typing import Any, Callable

from ..models import Apartment, Studio, TwoRoom, House, Penthouse


class EstateFactory:
    """
    Фабрика для создания объектов недвижимости.

    Хранит словарь типов. Создаёт объект по строковому
    идентификатору. Позволяет регистрировать новые типы
    через декоратор.
    """

    _registry = {
        "apartment": Apartment,
        "studio": Studio,
        "two_room": TwoRoom,
        "house": House,
        "penthouse": Penthouse,
    }

    @classmethod
    def create(cls, kind: str, **kwargs: Any) -> Any:
        """
        Создаёт объект указанного типа.

        Если тип неизвестен, выбрасывает ValueError
        с перечислением доступных типов.
        """
        if kind not in cls._registry:
            raise ValueError(
                f"Неизвестный тип: {kind!r}. "
                f"Доступные: {list(cls._registry.keys())}"
            )
        return cls._registry[kind](**kwargs)

    @classmethod
    def register(cls, kind: str) -> Callable[[type], type]:
        """
        Декоратор для регистрации нового типа.

        Использование:
            @EstateFactory.register("villa")
            class Villa(Apartment): ...
        """
        def decorator(klass: type) -> type:
            """Добавляет класс в реестр фабрики."""
            cls._registry[kind] = klass
            return klass
        return decorator

    @classmethod
    def list_kinds(cls) -> list[str]:
        """Возвращает список зарегистрированных типов."""
        return list(cls._registry.keys())
