
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from .base_engine import BaseEngine, CalculationResult, ReasoningStep
from ..utils.calendar import convert_to_lunar
from ..utils.bazi_utils import GANZHI_HOURS


SHIERYUEJIANG = {
    "子": "神后", "丑": "大吉", "寅": "功曹", "卯": "太冲",
    "辰": "天罡", "巳": "太乙", "午": "胜光", "未": "小吉",
    "申": "传送", "酉": "从魁", "戌": "河魁", "亥": "登明"
}

GUISHEN = {
    "子": "贵", "丑": "青", "寅": "六", "卯": "朱",
    "辰": "勾", "巳": "蛇", "午": "后", "未": "阴",
    "申": "玄", "酉": "常", "戌": "白", "亥": "空"
}

GANZHI_12 = [
    "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"
]


class LiurenEngine(BaseEngine):
    DOMAIN: str = "liuren"

    def __init__(self, rules: Optional[Dict[str, Any]] = None):
        super().__init__(rules)
        self._load_rules()

    def _load_rules(self):
        if not self.rules:
            self.rules = {
                "version": "1.0.0",
                "source": "《大六壬指南》《大六壬统宗》",
                "schools": ["古法", "现代"]
            }

    def calculate(self, birth_date: datetime, birth_time: str, 
                  timezone: str, location: str) -> CalculationResult:
        self.clear_reasoning_chain()
        
        try:
            lunar_date = convert_to_lunar(birth_date)
            day_ganzhi = self._get_day_ganzhi(birth_date)
            hour_zhi = self._get_hour_zhi(birth_date, birth_time)
            
            self.add_reasoning_step(
                rule_id="liuren.time.convert",
                description="时间转换为干支",
                input_data={"solar_date": birth_date.isoformat(), "birth_time": birth_time},
                output_data={"lunar_date": lunar_date, "day_ganzhi": day_ganzhi, "hour_zhi": hour_zhi},
                confidence=1.0
            )
            
            yuejiang = self._get_yuejiang(day_ganzhi)
            
            self.add_reasoning_step(
                rule_id="liuren.yuejiang",
                description="确定月将",
                input_data={"day_ganzhi": day_ganzhi},
                output_data={"yuejiang": yuejiang},
                confidence=1.0
            )
            
            guishen = self._get_guishen(day_ganzhi, hour_zhi)
            
            self.add_reasoning_step(
                rule_id="liuren.guishen",
                description="确定贵神",
                input_data={"day_ganzhi": day_ganzhi, "hour_zhi": hour_zhi},
                output_data={"guishen": guishen},
                confidence=0.98
            )
            
            liuchun = self._get_liuchun(day_ganzhi)
            
            self.add_reasoning_step(
                rule_id="liuren.liuchun",
                description="确定六亲",
                input_data={"day_ganzhi": day_ganzhi},
                output_data={"liuchun": liuchun},
                confidence=0.95
            )
            
            sanchuan = self._calculate_sanchuan(day_ganzhi, hour_zhi, liuchun)
            
            self.add_reasoning_step(
                rule_id="liuren.sanchuan",
                description="计算三传",
                input_data={"day_ganzhi": day_ganzhi, "hour_zhi": hour_zhi},
                output_data={"sanchuan": sanchuan},
                confidence=0.95
            )
            
            result = {
                "day_ganzhi": day_ganzhi,
                "hour_zhi": hour_zhi,
                "yuejiang": yuejiang,
                "guishen": guishen,
                "liuchun": liuchun,
                "sanchuan": sanchuan,
                "rules_version": self.rules.get("version", "1.0.0"),
                "school": self.rules.get("schools", ["古法"])[0]
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

    def _get_day_ganzhi(self, birth_date: datetime) -> str:
        base_date = datetime(1900, 1, 1)
        days = (birth_date.date() - base_date.date()).days
        ganzhi_index = (days + 6) % 60
        return GANZHI_HOURS[ganzhi_index]

    def _get_hour_zhi(self, birth_date: datetime, birth_time: str) -> str:
        hour = int(birth_time.split(":")[0])
        hour_zhi_index = (hour + 1) // 2 % 12
        return GANZHI_12[hour_zhi_index]

    def _get_yuejiang(self, day_ganzhi: str) -> str:
        day_zhi = day_ganzhi[-1]
        return SHIERYUEJIANG.get(day_zhi, "神后")

    def _get_guishen(self, day_ganzhi: str, hour_zhi: str) -> str:
        day_zhi = day_ganzhi[-1]
        day_zhi_index = GANZHI_12.index(day_zhi)
        hour_zhi_index = GANZHI_12.index(hour_zhi)
        
        yang_signs = ["子", "寅", "辰", "午", "申", "戌"]
        is_yang = day_zhi in yang_signs
        
        if is_yang:
            gui_start = 0
        else:
            gui_start = 12
        
        guishen_index = (gui_start + day_zhi_index - hour_zhi_index) % 12
        
        guishen_order = ["贵", "螣", "朱", "六", "勾", "青", "空", "白", "玄", "常", "阴", "后"]
        
        return guishen_order[guishen_index]

    def _get_liuchun(self, day_ganzhi: str) -> Dict[str, str]:
        day_stem = day_ganzhi[0]
        day_zhi = day_ganzhi[1]
        
        tiangan_wuxing = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
        dizhi_wuxing = {"子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火", "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水"}
        
        day_wuxing = tiangan_wuxing.get(day_stem, "")
        wuxing_cycle = ["木", "火", "土", "金", "水"]
        
        result = {}
        current_wuxing = day_wuxing
        
        for i, name in enumerate(["兄", "财", "官", "父", "子"]):
            idx = wuxing_cycle.index(current_wuxing)
            result[name] = wuxing_cycle[(idx + i) % 5]
            current_wuxing = wuxing_cycle[(idx + 1) % 5]
        
        return result

    def _calculate_sanchuan(self, day_ganzhi: str, hour_zhi: str, liuchun: Dict[str, str]) -> Dict[str, str]:
        day_zhi = day_ganzhi[1]
        day_zhi_index = GANZHI_12.index(day_zhi)
        
        initial_roll = (day_zhi_index + 10) % 12
        middle_roll = (initial_roll + 9) % 12
        final_roll = (middle_roll + 7) % 12
        
        return {
            "chuan": GANZHI_12[initial_roll],
            "zhong": GANZHI_12[middle_roll],
            "mo": GANZHI_12[final_roll]
        }

    def get_yuejiang_list(self) -> List[str]:
        return list(SHIERYUEJIANG.values())

    def get_guishen_list(self) -> List[str]:
        return ["贵", "螣蛇", "朱雀", "六合", "勾陈", "青龙", "天空", "白虎", "玄武", "太常", "太阴", "天后"]
