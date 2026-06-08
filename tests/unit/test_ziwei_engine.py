
import pytest
from datetime import datetime
from src.engines import ZiweiEngine


class TestZiweiEngine:
    
    def test_engine_initialization(self):
        engine = ZiweiEngine()
        assert engine.DOMAIN == "ziwei"
        assert "version" in engine.rules
    
    def test_calculate_basic(self):
        engine = ZiweiEngine()
        birth_date = datetime(2000, 1, 1)
        result = engine.calculate(birth_date, "12:00", "UTC+8", "北京")
        
        assert result.success is True
        assert "ziwei_palace" in result.result
        assert "palaces" in result.result
        assert "stars" in result.result
        assert "palace_analysis" in result.result
        assert result.confidence == 0.95
    
    def test_get_main_stars(self):
        engine = ZiweiEngine()
        stars = engine.get_main_stars()
        
        assert len(stars) == 14
        assert "紫微" in stars
        assert "天机" in stars
        assert "太阳" in stars
        assert "武曲" in stars
        assert "天同" in stars
        assert "廉贞" in stars
        assert "天府" in stars
        assert "太阴" in stars
        assert "贪狼" in stars
        assert "巨门" in stars
        assert "天相" in stars
        assert "天梁" in stars
        assert "七杀" in stars
        assert "破军" in stars
    
    def test_get_palace_info(self):
        engine = ZiweiEngine()
        palace = engine.get_palace_info("命宫")
        
        assert palace is not None
        assert "position" in palace
        assert "description" in palace
    
    def test_palace_positions(self):
        engine = ZiweiEngine()
        birth_date = datetime(2000, 1, 1)
        result = engine.calculate(birth_date, "12:00", "UTC+8", "北京")
        
        palaces = result.result.get("palaces", {})
        expected_palaces = ["命宫", "兄弟", "夫妻", "子女", "财帛", "疾厄", 
                           "迁移", "交友", "事业", "田宅", "福德", "父母"]
        
        for palace in expected_palaces:
            assert palace in palaces
    
    def test_reasoning_chain(self):
        engine = ZiweiEngine()
        birth_date = datetime(2000, 1, 1)
        result = engine.calculate(birth_date, "12:00", "UTC+8", "北京")
        
        reasoning_chain = result.reasoning_chain
        assert len(reasoning_chain) > 0
        
        step_ids = [step.rule_id for step in reasoning_chain]
        assert "ziwei.palace.ziwei" in step_ids
        assert "ziwei.palace.positions" in step_ids
        assert "ziwei.stars.allocation" in step_ids
