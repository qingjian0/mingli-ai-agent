
import pytest
from datetime import datetime
from src.engines import TaiyiEngine


class TestTaiyiEngine:
    
    def test_engine_initialization(self):
        engine = TaiyiEngine()
        assert engine.DOMAIN == "taiyi"
        assert "version" in engine.rules
    
    def test_calculate_basic(self):
        engine = TaiyiEngine()
        birth_date = datetime(2000, 1, 1)
        result = engine.calculate(birth_date, "12:00", "UTC+8", "北京")
        
        assert result.success is True
        assert "jushu" in result.result
        assert "taiyi_position" in result.result
        assert "wenwang" in result.result
        assert "tongyun" in result.result
        assert result.confidence == 0.9
    
    def test_get_jiugong_info(self):
        engine = TaiyiEngine()
        jiugong = engine.get_jiugong_info()
        
        assert len(jiugong) == 9
        assert "一宫坎" in jiugong
        assert "二宫坤" in jiugong
        assert "三宫震" in jiugong
        assert "四宫巽" in jiugong
        assert "五宫中" in jiugong
        assert "六宫乾" in jiugong
        assert "七宫兑" in jiugong
        assert "八宫艮" in jiugong
        assert "九宫离" in jiugong
    
    def test_interpret_jushu(self):
        engine = TaiyiEngine()
        assert engine.interpret_jushu(1) == "上元太乙局"
        assert engine.interpret_jushu(25) == "中元太乙局"
        assert engine.interpret_jushu(49) == "下元太乙局"
    
    def test_reasoning_chain(self):
        engine = TaiyiEngine()
        birth_date = datetime(2000, 1, 1)
        result = engine.calculate(birth_date, "12:00", "UTC+8", "北京")
        
        reasoning_chain = result.reasoning_chain
        assert len(reasoning_chain) >= 3
        
        step_ids = [step.rule_id for step in reasoning_chain]
        assert any("jushu" in step_id for step_id in step_ids)
        assert any("position" in step_id for step_id in step_ids)
        assert any("tongyun" in step_id for step_id in step_ids)
