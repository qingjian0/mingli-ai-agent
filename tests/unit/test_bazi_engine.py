
import pytest
from datetime import datetime
from src.engines import BaziEngine


class TestBaziEngine:
    
    def test_engine_initialization(self):
        engine = BaziEngine()
        assert engine.DOMAIN == "bazi"
        assert "version" in engine.rules
    
    def test_calculate_basic(self):
        engine = BaziEngine()
        birth_date = datetime(2000, 1, 1)
        result = engine.calculate(birth_date, "12:00", "UTC+8", "北京")
        
        assert result.success is True
        assert "bazi_pillar" in result.result
        assert "daymaster" in result.result
        assert "ten_gods" in result.result
        assert "wuxing" in result.result
        assert result.confidence == 0.99
    
    def test_calculate_with_different_time(self):
        engine = BaziEngine()
        
        result_morning = engine.calculate(datetime(2000, 1, 1), "08:00", "UTC+8", "北京")
        result_night = engine.calculate(datetime(2000, 1, 1), "20:00", "UTC+8", "北京")
        
        assert result_morning.success
        assert result_night.success
        assert result_morning.result["hour"]["branch"] != result_night.result["hour"]["branch"]
    
    def test_reasoning_chain(self):
        engine = BaziEngine()
        birth_date = datetime(2000, 1, 1)
        result = engine.calculate(birth_date, "12:00", "UTC+8", "北京")
        
        reasoning_chain = result.reasoning_chain
        assert len(reasoning_chain) > 0
        
        step_ids = [step.rule_id for step in reasoning_chain]
        assert "bazi.calendar.convert" in step_ids
        assert "bazi.pillar.year" in step_ids
        assert "bazi.pillar.month" in step_ids
        assert "bazi.pillar.day" in step_ids
        assert "bazi.pillar.hour" in step_ids
    
    def test_wuxing_calculation(self):
        engine = BaziEngine()
        result = engine.calculate(datetime(2000, 1, 1), "12:00", "UTC+8", "北京")
        
        wuxing = result.result.get("wuxing", {})
        assert "金" in wuxing
        assert "木" in wuxing
        assert "水" in wuxing
        assert "火" in wuxing
        assert "土" in wuxing
    
    def test_ten_gods_calculation(self):
        engine = BaziEngine()
        result = engine.calculate(datetime(2000, 1, 1), "12:00", "UTC+8", "北京")
        
        ten_gods = result.result.get("ten_gods", {})
        assert isinstance(ten_gods, dict)
    
    def test_nayin_calculation(self):
        engine = BaziEngine()
        result = engine.calculate(datetime(2000, 1, 1), "12:00", "UTC+8", "北京")
        
        nayin = result.result.get("nayin", {})
        assert "year" in nayin
        assert "month" in nayin
        assert "day" in nayin
        assert "hour" in nayin
