"""
Дескриптор для проверки диапазона значений.

Используется для полей, которые должны быть числами
в определённом диапазоне. Один дескриптор может применяться
к нескольким полям разных классов.
"""


class RangeDescriptor:
    """
    Дескриптор диапазона.

    При записи значения проверяет, что оно является числом
    и находится в диапазоне [min_value, max_value].
    Значение хранится в instance.__dict__ под именем поля.
    """

    def __init__(self, min_value: int | float, max_value: int | float) -> None:
        """Задаёт включённые границы допустимого диапазона."""
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner: type, name: str) -> None:
        """
        Вызывается автоматически при создании класса.

        Python сообщает дескриптору, под каким именем он
        используется в классе. Это позволяет сохранять значение
        в instance.__dict__ под правильным ключом.
        """
        self.name = name

    def __get__(
        self,
        instance: object | None,
        owner: type | None = None,
    ) -> object:
        """
        Возвращает значение при чтении атрибута.

        Если обращаются через класс (instance is None),
        возвращается сам дескриптор.
        """
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance: object, value: object) -> None:
        """
        Проверяет и сохраняет значение при записи.

        Если значение не число — выбрасывается TypeError.
        Если значение вне диапазона — выбрасывается ValueError.
        """
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError(f"{self.name} должно быть числом")

        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"{self.name} должно быть от {self.min_value} "
                f"до {self.max_value}"
            )

        instance.__dict__[self.name] = value
