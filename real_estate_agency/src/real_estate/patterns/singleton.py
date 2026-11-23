"""
Метакласс для паттерна Singleton.

Паттерн Singleton (глава 24). Гарантирует, что у класса
будет только один экземпляр. Метакласс перехватывает
создание объекта через __call__ (глава 23).
"""


from typing import Any


class SingletonMeta(type):
    """
    Метакласс, превращающий класс в Singleton.

    Хранит словарь экземпляров по классам. При создании
    объекта проверяет, есть ли уже экземпляр данного класса.
    Если есть — возвращает его. Если нет — создаёт новый.
    """

    _instances = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Перехватывает создание объекта."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
