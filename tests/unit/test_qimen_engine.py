
import pytest
from datetime import datetime
from src.engines import QimenEngine


class TestQimenEngine:
    
    def test_engine_initialization(self):
        engine = QimenEngine()
        assert engine.DOMAIN == "qimen"
        assert "version" in engine.rules
    
    def test_calculate_basic(self):
        engine = QimenEngine()
        birth_date = datetime(2000, 1, 1)
        result = engine.calculate(birth_date, "12:00", "UTC+8", "北京")
        
        assert result.success is True
        assert "hour_ganzhi" in result.result
        assert "pan_type" in result.result
        assert "gong_positions" in result.result
        assert "bamen" in result.result
        assert "jiuxing" in result.result
        assert "bashen" in result.result
        assert result.confidence == 0.95
    
    def test_get_jiuxing_info(self):
        engine = QimenEngine()
        stars = engine.get_jiuxing_info()
        
        assert len(stars) == 9
        assert "天蓬" in stars
        assert "天芮" in stars
        assert "天冲" in stars
        assert "天辅" in stars
        assert "天禽" in stars
        assert "天心" in stars
        assert "天柱" in stars
        assert "天任" in stars
        assert "天英" in stars
    
    def test_get_bamen_info(self):
        engine = QimenEngine()
        doors = engine.get_bamen_info()
        
        assert len(doors) == 8
        assert "休门" in doors
        assert "生门" in doors
        assert "伤门" in doors
        assert "杜门" in doors
        assert "景门" in doors
        assert "死门" in doors
        assert "惊门" in doors
        assert "开门" in doors
    
    def test_reasoning_chain(self):
        engine = QimenEngine()
        birth_date = datetime(2000, 1, 1)
        result = engine.calculate(birth_date, "12:00", "UTC+8", "北京")
        
        reasoning_chain = result.reasoning_chain
        assert len(reasoning_chain) >= 3
        
        step_ids = [step.rule_id for step in reasoning_chain]
        assert any("time.convert" in step_id for step_id in step_ids)
        assert any("jifen.calculate" in step_id for step_id in step_ids)
        assert any("positions.calculate" in step_id for step_id in step_ids)
