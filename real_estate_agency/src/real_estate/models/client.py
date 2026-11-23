"""
Клиент и агент.

Демонстрируют:
- утиную типизацию (глава 30)
- Observer (глава 26) — у Client есть update()
"""

from dataclasses import dataclass, field

@dataclass
class Client:
    """Клиент агентства. Подписывается на уведомления."""

    name: str
    budget: int = 0
    notifications: list[str] = field(default_factory=list, repr=False)

    def describe(self) -> str:
        """Описание клиента."""
        return f"Клиент {self.name}, бюджет {self.budget} ₽"

    def update(self, event: object) -> None:
        """Реакция на уведомление (Observer, глава 26)."""
        message = f"{self.name}: {event}"
        self.notifications.append(message)
        print(f"  → {message}")

@dataclass
class Agent:
    """Агент агентства."""

    name: str
    experience: int

    def describe(self) -> str:
        """Описание агента."""
        return f"Агент {self.name}, стаж {self.experience} лет"

