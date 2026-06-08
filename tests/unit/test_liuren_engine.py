
import pytest
from datetime import datetime
from src.engines import LiurenEngine


class TestLiurenEngine:
    
    def test_engine_initialization(self):
        engine = LiurenEngine()
        assert engine.DOMAIN == "liuren"
        assert "version" in engine.rules
    
    def test_calculate_basic(self):
        engine = LiurenEngine()
        birth_date = datetime(2000, 1, 1)
        result = engine.calculate(birth_date, "12:00", "UTC+8", "北京")
        
        assert result.success is True
        assert "hour_zhi" in result.result
        assert "yuejiang" in result.result
        assert "guishen" in result.result
        assert "liuchun" in result.result
        assert "sanchuan" in result.result
        assert result.confidence == 0.95
    
    def test_get_yuejiang_list(self):
        engine = LiurenEngine()
        yuejiang = engine.get_yuejiang_list()
        
        assert len(yuejiang) == 12
        assert "神后" in yuejiang
        assert "大吉" in yuejiang
        assert "功曹" in yuejiang
        assert "太冲" in yuejiang
        assert "天罡" in yuejiang
        assert "太乙" in yuejiang
        assert "胜光" in yuejiang
        assert "小吉" in yuejiang
        assert "传送" in yuejiang
        assert "从魁" in yuejiang
        assert "河魁" in yuejiang
        assert "登明" in yuejiang
    
    def test_get_guishen_list(self):
        engine = LiurenEngine()
        guishen = engine.get_guishen_list()
        
        assert len(guishen) == 12
        assert "贵" in guishen
        assert "螣蛇" in guishen
        assert "朱雀" in guishen
        assert "六合" in guishen
        assert "勾陈" in guishen
        assert "青龙" in guishen
        assert "天空" in guishen
        assert "白虎" in guishen
        assert "玄武" in guishen
        assert "太常" in guishen
        assert "太阴" in guishen
        assert "天后" in guishen
    
    def test_reasoning_chain(self):
        engine = LiurenEngine()
        birth_date = datetime(2000, 1, 1)
        result = engine.calculate(birth_date, "12:00", "UTC+8", "北京")
        
        reasoning_chain = result.reasoning_chain
        assert len(reasoning_chain) >= 4
        
        step_ids = [step.rule_id for step in reasoning_chain]
        assert any("time.convert" in step_id for step_id in step_ids)
        assert any("yuejiang" in step_id for step_id in step_ids)
        assert any("guishen" in step_id for step_id in step_ids)
        assert any("sanchuan" in step_id for step_id in step_ids)
