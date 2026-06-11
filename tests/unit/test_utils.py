
import pytest
from datetime import datetime
from src.utils import (
    TIANGAN, DIZHI, TIANGAN_WUXING, DIZHI_WUXING,
    get_year_stem, get_month_stem, get_day_stem_branch, get_hour_stem,
    calculate_shishen, get_nayin, convert_to_lunar, get_solar_term
)


class TestBaziUtils:
    
    def test_tiangan_list(self):
        assert len(TIANGAN) == 10
        assert "甲" in TIANGAN
        assert "癸" in TIANGAN
    
    def test_dizhi_list(self):
        assert len(DIZHI) == 12
        assert "子" in DIZHI
        assert "亥" in DIZHI
    
    def test_tiangan_wuxing(self):
        assert TIANGAN_WUXING["甲"] == "木"
        assert TIANGAN_WUXING["丙"] == "火"
        assert TIANGAN_WUXING["戊"] == "土"
        assert TIANGAN_WUXING["庚"] == "金"
        assert TIANGAN_WUXING["壬"] == "水"
    
    def test_dizhi_wuxing(self):
        assert "水" in DIZHI_WUXING["子"]
        assert "木" in DIZHI_WUXING["寅"]
        assert "火" in DIZHI_WUXING["午"]
        assert "金" in DIZHI_WUXING["申"]
        assert "土" in DIZHI_WUXING["辰"]
    
    def test_get_year_stem(self):
        assert get_year_stem(2024) == "甲"
        assert get_year_stem(2025) == "乙"
    
    def test_get_month_stem(self):
        assert get_month_stem("甲", 1) == "丙"
        assert get_month_stem("甲", 2) == "戊"
    
    def test_get_day_stem_branch(self):
        stem, branch = get_day_stem_branch(datetime(2024, 1, 1))
        assert stem in TIANGAN
        assert branch in DIZHI
    
    def test_get_hour_stem(self):
        assert get_hour_stem("甲", 0) == "甲"
        assert get_hour_stem("甲", 1) == "丙"
    
    def test_calculate_shishen(self):
        ten_gods = calculate_shishen("甲", ["甲", "乙", "丙"])
        assert "比肩" in ten_gods
        assert "劫财" in ten_gods
        assert "食神" in ten_gods
    
    def test_get_nayin(self):
        assert get_nayin("甲", "子") == "海中金"
        assert get_nayin("丙", "寅") == "炉中火"


class TestCalendarUtils:
    
    def test_convert_to_lunar(self):
        lunar = convert_to_lunar(datetime(2024, 1, 1))
        assert "year" in lunar
        assert "month" in lunar
        assert "day" in lunar
    
    def test_get_solar_term(self):
        term = get_solar_term(datetime(2024, 2, 4))
        assert isinstance(term, str)
