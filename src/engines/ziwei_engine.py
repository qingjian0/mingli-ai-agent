
from datetime import datetime
from typing import Dict, Any, Optional, Tuple, List
from .base_engine import BaseEngine, CalculationResult, ReasoningStep
from ..utils.calendar import convert_to_lunar
from ..utils.ziwei_utils import (
    STARS, PALACES, get_ziwei_palace, get_stars_by_birth,
    calculate_palace_positions, analyze_stars_in_palace
)


class ZiweiEngine(BaseEngine):
    DOMAIN: str = "ziwei"

    def __init__(self, rules: Optional[Dict[str, Any]] = None):
        super().__init__(rules)
        self._load_rules()

    def _load_rules(self):
        if not self.rules:
            self.rules = {
                "version": "1.0.0",
                "source": "《紫微斗数全书》",
                "schools": ["南派", "北派", "现代派"]
            }

    def calculate(self, birth_date: datetime, birth_time: str, 
                  timezone: str, location: str) -> CalculationResult:
        self.clear_reasoning_chain()
        
        try:
            lunar_date = convert_to_lunar(birth_date)
            
            ziwei_palace = get_ziwei_palace(lunar_date["year"], lunar_date["month"], 
                                          lunar_date["day"], birth_time)
            
            self.add_reasoning_step(
                rule_id="ziwei.palace.ziwei",
                description="确定紫微宫位置",
                input_data={"lunar_date": lunar_date, "birth_time": birth_time},
                output_data={"ziwei_palace": ziwei_palace},
                confidence=1.0
            )
            
            palace_positions = calculate_palace_positions(ziwei_palace)
            
            self.add_reasoning_step(
                rule_id="ziwei.palace.positions",
                description="计算十二宫位置",
                input_data={"ziwei_palace": ziwei_palace},
                output_data={"palaces": palace_positions},
                confidence=1.0
            )
            
            stars = get_stars_by_birth(lunar_date["year"], birth_time)
            
            self.add_reasoning_step(
                rule_id="ziwei.stars.allocation",
                description="分配十四主星及杂曜",
                input_data={"lunar_year": lunar_date["year"], "birth_time": birth_time},
                output_data={"stars_count": len(stars)},
                confidence=1.0
            )
            
            palace_analysis = {}
            for palace_name, position in palace_positions.items():
                palace_analysis[palace_name] = analyze_stars_in_palace(position, stars)
            
            self.add_reasoning_step(
                rule_id="ziwei.analysis.palace",
                description="分析各宫位星曜组合",
                input_data={"palaces": palace_positions, "stars": stars},
                output_data={"analysis_count": len(palace_analysis)},
                confidence=0.95
            )
            
            result = {
                "ziwei_palace": ziwei_palace,
                "palaces": palace_positions,
                "stars": stars,
                "palace_analysis": palace_analysis,
                "rules_version": self.rules.get("version", "1.0.0"),
                "school": self.rules.get("schools", ["南派"])[0]
            }
            
            return CalculationResult(
                success=True,
                result=result,
                reasoning_chain=self.get_reasoning_chain(),
                confidence=0.95
            )
            
        except Exception as e:
            return CalculationResult(
                success=False,
                result={},
                reasoning_chain=self.get_reasoning_chain(),
                confidence=0.0,
                error=str(e)
            )

    def get_main_stars(self) -> List[str]:
        return [star["name"] for star in STARS["main"]]

    def get_palace_info(self, palace_name: str) -> Optional[Dict[str, Any]]:
        return PALACES.get(palace_name)
