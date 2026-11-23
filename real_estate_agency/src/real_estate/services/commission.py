"""
Стратегии расчёта комиссии.

Паттерн Strategy (глава 34). Позволяет менять способ
расчёта комиссии без изменения сервиса сделок.
"""

from abc import ABC, abstractmethod


class CommissionStrategy(ABC):
    """
    Абстрактная стратегия расчёта комиссии.

    Наследники обязаны реализовать calculate.
    """

    @abstractmethod
    def calculate(self, price: int) -> float:
        """Рассчитывает комиссию от цены."""
        ...


class FixedCommission(CommissionStrategy):
    """Фиксированная комиссия."""

    def __init__(self, amount: int = 50_000) -> None:
        """Сохраняет фиксированную сумму комиссии."""
        if amount < 0:
            raise ValueError("Комиссия не может быть отрицательной")
        self.amount = amount

    def calculate(self, price: int) -> float:
        """Возвращает фиксированную сумму."""
        return self.amount


class PercentCommission(CommissionStrategy):
    """Процентная комиссия."""

    def __init__(self, rate: float = 0.03) -> None:
        """Сохраняет ставку комиссии в долях от единицы."""
        if not 0 <= rate <= 1:
            raise ValueError("Ставка комиссии должна быть от 0 до 1")
        self.rate = rate

    def calculate(self, price: int) -> float:
        """Возвращает процент от цены."""
        return price * self.rate


class LoyaltyCommission(PercentCommission):
    """
    Льготная комиссия для постоянных клиентов.

    Наследует логику процентной комиссии,
    но с уменьшенной ставкой.
    """

    def __init__(self) -> None:
        """Настраивает льготную ставку 1.5 процента."""
        super().__init__(rate=0.015)


class CommissionCalculator:
    """Вызываемый объект для применения стратегии комиссии."""

    def __new__(
        cls,
        strategy: CommissionStrategy | type[CommissionStrategy],
    ) -> "CommissionCalculator":
        """Создаёт калькулятор и принимает класс или стратегию."""
        instance = super().__new__(cls)
        if isinstance(strategy, type):
            strategy = strategy()
        if not isinstance(strategy, CommissionStrategy):
            raise TypeError("Нужен объект или класс CommissionStrategy")
        instance.strategy = strategy
        return instance

    def __init__(
        self,
        strategy: CommissionStrategy | type[CommissionStrategy],
    ) -> None:
        """Стратегия уже сохранена в __new__."""

    def __call__(self, price: int) -> float:
        """Рассчитывает комиссию как обычный вызов функции."""
        return self.strategy.calculate(price)
