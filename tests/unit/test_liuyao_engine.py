
import pytest
from datetime import datetime
from src.engines import LiuyaoEngine


class TestLiuyaoEngine:
    
    def test_engine_initialization(self):
        engine = LiuyaoEngine()
        assert engine.DOMAIN == "liuyao"
        assert "version" in engine.rules
    
    def test_calculate_basic(self):
        engine = LiuyaoEngine()
        birth_date = datetime(2000, 1, 1)
        result = engine.calculate(birth_date, "12:00", "UTC+8", "北京")
        
        assert result.success is True
        assert "gua" in result.result
        assert "liuqin" in result.result
        assert "liushen" in result.result
        assert result.confidence == 0.95
    
    def test_get_liuqi_info(self):
        engine = LiuyaoEngine()
        liuqi = engine.get_liuqi_info()
        
        assert len(liuqi) == 6
        assert "青龙" in liuqi
        assert "朱雀" in liuqi
        assert "勾陈" in liuqi
        assert "螣蛇" in liuqi
        assert "白虎" in liuqi
        assert "玄武" in liuqi
    
    def test_get_liuqin_info(self):
        engine = LiuyaoEngine()
        liuqin = engine.get_liuqin_info()
        
        assert len(liuqin) == 5
        assert "父母" in liuqin
        assert "兄弟" in liuqin
        assert "子孙" in liuqin
        assert "妻财" in liuqin
        assert "官鬼" in liuqin
    
    def test_reasoning_chain(self):
        engine = LiuyaoEngine()
        birth_date = datetime(2000, 1, 1)
        result = engine.calculate(birth_date, "12:00", "UTC+8", "北京")
        
        reasoning_chain = result.reasoning_chain
        assert len(reasoning_chain) >= 3
        
        step_ids = [step.rule_id for step in reasoning_chain]
        assert any("yuejian" in step_id for step_id in step_ids)
        assert any("gua" in step_id for step_id in step_ids)
        assert any("liuqin" in step_id for step_id in step_ids)
