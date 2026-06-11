
import pytest
from datetime import datetime
from src.engines import BaziEngine, ZiweiEngine


@pytest.fixture
def bazi_engine():
    return BaziEngine()


@pytest.fixture
def ziwei_engine():
    return ZiweiEngine()


@pytest.fixture
def test_birth_date():
    return datetime(2000, 1, 1)


@pytest.fixture
def test_birth_time():
    return "12:00"


@pytest.fixture
def test_timezone():
    return "UTC+8"


@pytest.fixture
def test_location():
    return "北京"
