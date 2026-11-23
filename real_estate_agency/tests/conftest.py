"""
Общие фикстуры для тестов.

pytest находит этот файл автоматически. Фикстуры доступны
во всех тестах без импорта.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from real_estate.models import Apartment, House
from real_estate.services import EstateStorage


@pytest.fixture
def sample_apartment():
    """Свежая квартира для теста."""
    return Apartment("ул. Ленина, д. 10, кв. 5", 65, 8_500_000)


@pytest.fixture
def sample_house():
    """Свежий дом для теста."""
    return House("ул. Садовая, д. 3", 200, 2)


@pytest.fixture
def sample_storage():
    """Пустое хранилище для теста."""
    return EstateStorage()


@pytest.fixture
def sample_db_path(tmp_path):
    """Временный путь к базе данных."""
    return str(tmp_path / "test.db")
