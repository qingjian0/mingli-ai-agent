
import pytest
from datetime import datetime
from src.engines import MeihuaEngine


class TestMeihuaEngine:
    
    def test_engine_initialization(self):
        engine = MeihuaEngine()
        assert engine.DOMAIN == "meihua"
        assert "version" in engine.rules
    
    def test_calculate_basic(self):
        engine = MeihuaEngine()
        birth_date = datetime(2000, 1, 1)
        result = engine.calculate(birth_date, "12:00", "UTC+8", "北京")
        
        assert result.success is True
        assert "shang_gua" in result.result
        assert "xia_gua" in result.result
        assert "dong_yao" in result.result
        assert "ti_yong" in result.result
        assert result.confidence == 0.95
    
    def test_get_bagua_info(self):
        engine = MeihuaEngine()
        bagua = engine.get_bagua_info()
        
        assert len(bagua) == 8
        bagua_names = [gua["name"] for gua in bagua]
        assert "乾" in bagua_names
        assert "兑" in bagua_names
        assert "离" in bagua_names
        assert "震" in bagua_names
        assert "巽" in bagua_names
        assert "坎" in bagua_names
        assert "艮" in bagua_names
        assert "坤" in bagua_names
    
    def test_reasoning_chain(self):
        engine = MeihuaEngine()
        birth_date = datetime(2000, 1, 1)
        result = engine.calculate(birth_date, "12:00", "UTC+8", "北京")
        
        reasoning_chain = result.reasoning_chain
        assert len(reasoning_chain) >= 3
        
        step_ids = [step.rule_id for step in reasoning_chain]
        assert any("shang_gua" in step_id for step_id in step_ids)
        assert any("xia_gua" in step_id for step_id in step_ids)
        assert any("ti_yong" in step_id for step_id in step_ids)
