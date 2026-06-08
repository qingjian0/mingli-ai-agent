
from datetime import datetime
from typing import Dict, Any, Optional, List
from .base_engine import BaseEngine, CalculationResult, ReasoningStep


JIUGONG_TAIYI = ["一宫坎", "二宫坤", "三宫震", "四宫巽", "五宫中", "六宫乾", "七宫兑", "八宫艮", "九宫离"]

WENWANG_PAIBI = ["太乙", "文昌", "始击", "文曲", "计都", "青龙", "螣蛇", "太阴", "白虎", "玄武"]

WUYUN = ["水", "火", "木", "金", "土"]


class TaiyiEngine(BaseEngine):
    DOMAIN: str = "taiyi"

    def __init__(self, rules: Optional[Dict[str, Any]] = None):
        super().__init__(rules)
        self._load_rules()

    def _load_rules(self):
        if not self.rules:
            self.rules = {
                "version": "1.0.0",
                "source": "《太乙数精义》《太乙遁甲秘典》",
                "schools": ["传统推演", "局数应用"]
            }

    def calculate(self, birth_date: datetime, birth_time: str, 
                  timezone: str, location: str) -> CalculationResult:
        self.clear_reasoning_chain()
        
        try:
            year = birth_date.year
            month = birth_date.month
            day = birth_date.day
            
            jushu = self._calculate_jushu(year)
            
            self.add_reasoning_step(
                rule_id="taiyi.jushu",
                description="计算局数",
                input_data={"year": year},
                output_data={"jushu": jushu},
                confidence=0.98
            )
            
            taiyi_position = self._calculate_taiyi_position(jushu)
            
            self.add_reasoning_step(
                rule_id="taiyi.position",
                description="计算太乙位置",
                input_data={"jushu": jushu},
                output_data={"taiyi_position": taiyi_position},
                confidence=0.95
            )
            
            wenwang = self._calculate_wenwang_paibi(jushu)
            
            self.add_reasoning_step(
                rule_id="taiyi.wenwang",
                description="计算文王排法",
                input_data={"jushu": jushu},
                output_data={"wenwang": wenwang},
                confidence=0.95
            )
            
            tongyun = self._calculate_tongyun(year)
            
            self.add_reasoning_step(
                rule_id="taiyi.tongyun",
                description="计算统运",
                input_data={"year": year},
                output_data={"tongyun": tongyun},
                confidence=0.90
            )
            
            result = {
                "year": year,
                "month": month,
                "day": day,
                "jushu": jushu,
                "taiyi_position": taiyi_position,
                "wenwang": wenwang,
                "tongyun": tongyun,
                "rules_version": self.rules.get("version", "1.0.0"),
                "school": self.rules.get("schools", ["传统推演"])[0]
            }
            
            return CalculationResult(
                success=True,
                result=result,
                reasoning_chain=self.get_reasoning_chain(),
                confidence=0.90
            )
            
        except Exception as e:
            return CalculationResult(
                success=False,
                result={},
                reasoning_chain=self.get_reasoning_chain(),
                confidence=0.0,
                error=str(e)
            )

    def _calculate_jushu(self, year: int) -> int:
        base_year = 1984
        
        years_since_base = year - base_year
        
        jushu = (years_since_base % 72) + 1
        
        return jushu

    def _calculate_taiyi_position(self, jushu: int) -> int:
        position = (jushu * 3) % 9
        
        position_map = {
            1: 0, 2: 3, 3: 6,
            4: 1, 5: 4, 6: 7,
            7: 2, 8: 5, 0: 8
        }
        
        return position_map.get(position, 0)

    def _calculate_wenwang_paibi(self, jushu: int) -> List[Dict[str, Any]]:
        paibi = []
        
        for i in range(10):
            pos = (jushu + i * 7) % 9
            paibi.append({
                "name": WENWANG_PAIBI[i],
                "position": pos,
                "palace": JIUGONG_TAIYI[pos]
            })
        
        return paibi

    def _calculate_tongyun(self, year: int) -> Dict[str, Any]:
        base_year = 1984
        
        years_since_base = year - base_year
        
        cycle = years_since_base // 60
        year_in_cycle = years_since_base % 60
        
        yun_index = (year_in_cycle // 12) % 5
        wuyun = WUYUN[yun_index]
        
        if year_in_cycle < 30:
            tongyun = "阳九百六"
            description = "阳气旺盛，大有作为"
        else:
            tongyun = "阴六百三"
            description = "阴气渐盛，静待时机"
        
        return {
            "cycle": cycle + 1,
            "year_in_cycle": year_in_cycle,
            "wuyun": wuyun,
            "tongyun": tongyun,
            "description": description
        }

    def get_jiugong_info(self) -> List[str]:
        return JIUGONG_TAIYI

    def interpret_jushu(self, jushu: int) -> str:
        if jushu <= 24:
            return "上元太乙局"
        elif jushu <= 48:
            return "中元太乙局"
        else:
            return "下元太乙局"
