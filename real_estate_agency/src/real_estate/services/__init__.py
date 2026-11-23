"""
Экспорт всех сервисов.

Позволяет импортировать всё напрямую:

    from real_estate.services import EstateStorage, DealService
"""

from .storage import EstateStorage
from .commission import (
    CommissionStrategy,
    FixedCommission,
    PercentCommission,
    LoyaltyCommission,
    CommissionCalculator,
)
from .notification_service import (
    NotificationService,
    EmailNotifier,
    SmsNotifier,
)
from .deal_service import DealService
from .rental_service import RentalService
from .report_service import ReportService

__all__ = [
    "EstateStorage",
    "CommissionStrategy",
    "FixedCommission",
    "PercentCommission",
    "LoyaltyCommission",
    "CommissionCalculator",
    "NotificationService",
    "EmailNotifier",
    "SmsNotifier",
    "DealService",
    "RentalService",
    "ReportService",
]
