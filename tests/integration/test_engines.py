
import pytest
from datetime import datetime
from src.engines import (
    BaziEngine, ZiweiEngine, QimenEngine, 
    LiurenEngine, MeihuaEngine, LiuyaoEngine, TaiyiEngine
)


class TestAllEnginesIntegration:
    """所有引擎集成测试"""
    
    def test_all_engines_can_calculate(self):
        """测试所有引擎都能正常计算"""
        engines = {
            "bazi": BaziEngine(),
            "ziwei": ZiweiEngine(),
            "qimen": QimenEngine(),
            "liuren": LiurenEngine(),
            "meihua": MeihuaEngine(),
            "liuyao": LiuyaoEngine(),
            "taiyi": TaiyiEngine()
        }
        
        test_date = datetime(2000, 1, 1)
        test_time = "12:00"
        
        for name, engine in engines.items():
            result = engine.calculate(test_date, test_time, "UTC+8", "北京")
            assert result.success, f"{name} engine failed: {result.error}"
            assert result.confidence > 0, f"{name} engine has zero confidence"
            assert len(result.reasoning_chain) > 0, f"{name} engine has no reasoning chain"
    
    def test_all_engines_have_domain(self):
        """测试所有引擎都有正确的DOMAIN属性"""
        engines = [
            (BaziEngine(), "bazi"),
            (ZiweiEngine(), "ziwei"),
            (QimenEngine(), "qimen"),
            (LiurenEngine(), "liuren"),
            (MeihuaEngine(), "meihua"),
            (LiuyaoEngine(), "liuyao"),
            (TaiyiEngine(), "taiyi")
        ]
        
        for engine, expected_domain in engines:
            assert engine.DOMAIN == expected_domain
    
    def test_all_engines_have_rules(self):
        """测试所有引擎都有规则配置"""
        engines = [
            BaziEngine(),
            ZiweiEngine(),
            QimenEngine(),
            LiurenEngine(),
            MeihuaEngine(),
            LiuyaoEngine(),
            TaiyiEngine()
        ]
        
        for engine in engines:
            assert hasattr(engine, 'rules')
            assert isinstance(engine.rules, dict)
            assert 'version' in engine.rules
    
    def test_reasoning_chain_consistency(self):
        """测试推理链一致性"""
        engine = BaziEngine()
        result = engine.calculate(datetime(1990, 5, 15), "10:30", "UTC+8", "北京")
        
        assert result.success
        assert len(result.reasoning_chain) >= 4
        
        for step in result.reasoning_chain:
            assert hasattr(step, 'rule_id')
            assert hasattr(step, 'description')
            assert hasattr(step, 'input_data')
            assert hasattr(step, 'output_data')
            assert hasattr(step, 'confidence')
            assert 0 <= step.confidence <= 1
    
    def test_multiple_calculations_same_engine(self):
        """测试同一引擎多次计算"""
        engine = BaziEngine()
        
        dates = [
            datetime(1990, 1, 1),
            datetime(2000, 6, 15),
            datetime(2010, 12, 31)
        ]
        
        for date in dates:
            result = engine.calculate(date, "12:00", "UTC+8", "北京")
            assert result.success
            assert result.result['daymaster'] in ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
