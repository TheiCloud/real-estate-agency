"""Настройки проекта.

Все константы собраны в одном месте. Если нужно изменить
путь к базе или название агентства — правим здесь.
"""

from pathlib import Path

# Путь к файлу базы данных.
PROJECT_ROOT = Path(__file__).resolve().parent
DB_PATH = PROJECT_ROOT / "data" / "agency.db"

# Название агентства по умолчанию.
AGENCY_NAME = "Дом-Сервис"

# Уровень логирования (DEBUG, INFO, WARNING, ERROR).
LOG_LEVEL = "INFO"

# Ставка комиссии по умолчанию (3%).
DEFAULT_COMMISSION_RATE = 0.03

# Диапазон допустимой площади (м²).
MIN_AREA = 5
MAX_AREA = 500
