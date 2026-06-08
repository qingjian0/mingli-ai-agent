
from datetime import datetime
from typing import Dict, Any, Optional, List
from .base_engine import BaseEngine, CalculationResult, ReasoningStep
from ..utils.calendar import convert_to_lunar, get_solar_term


# 奇门遁甲常量
JIUGONG = ["坎一", "坤二", "震三", "巽四", "中五", "乾六", "兑七", "艮八", "离九"]

BAMEN = ["休门", "生门", "伤门", "杜门", "景门", "死门", "惊门", "开门"]

JIUXING = ["天蓬", "天芮", "天冲", "天辅", "天禽", "天心", "天柱", "天任", "天英"]

BASHEN = ["值符", "螣蛇", "太阴", "六合", "白虎", "玄武", "九地", "九天"]

SANQI = {"乙": "日奇", "丙": "月奇", "丁": "星奇"}

# 六十甲子（用于时辰计算）
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
GANZHI_60 = [TIANGAN[i % 10] + DIZHI[i % 12] for i in range(60)]


def _extract_num_from_chinese(text: str) -> int:
    chinese_nums = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
    for char, num in chinese_nums.items():
        if char in text:
            return num
    return 1


class QimenEngine(BaseEngine):
    DOMAIN: str = "qimen"

    def __init__(self, rules: Optional[Dict[str, Any]] = None):
        super().__init__(rules)
        self._load_rules()

    def _load_rules(self):
        if not self.rules:
            self.rules = {
                "version": "1.0.0",
                "source": "《奇门遁甲》《烟壤经》《奇门遁甲揭秘》",
                "schools": ["九星流", "天干流", "刻卦法"]
            }

    def calculate(self, birth_date: datetime, birth_time: str, 
                  timezone: str, location: str) -> CalculationResult:
        self.clear_reasoning_chain()
        
        try:
            lunar_date = convert_to_lunar(birth_date)
            solar_term = get_solar_term(birth_date)
            
            hour_ganzhi = self._get_hour_ganzhi(birth_date, birth_time)
            
            self.add_reasoning_step(
                rule_id="qimen.time.convert",
                description="时间转换",
                input_data={"solar_date": birth_date.isoformat(), "birth_time": birth_time},
                output_data={"lunar_date": lunar_date, "solar_term": solar_term, "hour_ganzhi": hour_ganzhi},
                confidence=1.0
            )
            
            jifen = self._calculate_jifen(birth_date, birth_time)
            pan_type = self._get_pan_type(jifen)
            pan_num = _extract_num_from_chinese(pan_type)
            
            self.add_reasoning_step(
                rule_id="qimen.jifen.calculate",
                description="计算节气积数",
                input_data={"birth_date": birth_date.isoformat(), "birth_time": birth_time},
                output_data={"jifen": jifen, "pan_type": pan_type},
                confidence=0.98
            )
            
            gong_positions = self._calculate_gong_positions(pan_num)
            men_positions = self._calculate_door_positions(pan_num)
            xing_positions = self._calculate_star_positions(pan_num)
            shen_positions = self._calculate_shen_positions(pan_num)
            
            self.add_reasoning_step(
                rule_id="qimen.positions.calculate",
                description="计算九宫八门九星八神",
                input_data={"pan_num": pan_num},
                output_data={"gong": gong_positions, "men": men_positions, "xing": xing_positions, "shen": shen_positions},
                confidence=0.95
            )
            
            sanqi = self._check_sanqi(gong_positions)
            
            result = {
                "hour_ganzhi": hour_ganzhi,
                "pan_type": pan_type,
                "gong_positions": gong_positions,
                "bamen": men_positions,
                "jiuxing": xing_positions,
                "bashen": shen_positions,
                "sanqi": sanqi,
                "rules_version": self.rules.get("version", "1.0.0"),
                "school": self.rules.get("schools", ["九星流"])[0]
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

    def _get_hour_ganzhi(self, birth_date: datetime, birth_time: str) -> str:
        hour = int(birth_time.split(":")[0])
        base_date = datetime(1900, 1, 1)
        days = (birth_date.date() - base_date.date()).days
        base_hour_ganzhi_index = (days * 12 + hour // 2) % 60
        return GANZHI_60[base_hour_ganzhi_index % 60]

    def _calculate_jifen(self, birth_date: datetime, birth_time: str) -> int:
        year = birth_date.year
        month = birth_date.month
        day = birth_date.day
        
        jieqi_dates = {
            1: 0, 2: 0, 3: 4, 4: 5, 5: 6, 6: 6, 7: 7, 8: 8,
            9: 8, 10: 9, 11: 10, 12: 10
        }
        
        hour = int(birth_time.split(":")[0])
        jifen = (year - 1984) * 360 + jieqi_dates.get(month, 0) * 30 + day + hour // 2
        
        return jifen

    def _get_pan_type(self, jifen: int) -> str:
        mod_9 = jifen % 9
        
        pan_types = {
            1: "阳遁一局",
            2: "阳遁二局",
            3: "阳遁三局",
            4: "阳遁四局",
            5: "阳遁五局",
            6: "阳遁六局",
            7: "阳遁七局",
            8: "阳遁八局",
            0: "阳遁九局"
        }
        
        return pan_types.get(mod_9, "阳遁一局")

    def _calculate_gong_positions(self, pan_num: int) -> Dict[str, int]:
        positions = {}
        for i, gong in enumerate(JIUGONG):
            positions[gong] = (i + pan_num - 1) % 9
        
        return positions

    def _calculate_door_positions(self, pan_num: int) -> Dict[str, int]:
        positions = {}
        for i, men in enumerate(BAMEN):
            positions[men] = (i + pan_num - 1) % 9
        
        return positions

    def _calculate_star_positions(self, pan_num: int) -> Dict[str, int]:
        positions = {}
        for i, xing in enumerate(JIUXING):
            positions[xing] = (i + pan_num - 1) % 9
        
        return positions

    def _calculate_shen_positions(self, pan_num: int) -> Dict[str, int]:
        positions = {}
        for i, shen in enumerate(BASHEN):
            positions[shen] = i
        
        return positions

    def _check_sanqi(self, gong_positions: Dict[str, int]) -> Dict[str, str]:
        sanqi_result = {}
        
        for qi_name, qi_desc in SANQI.items():
            for gong, pos in gong_positions.items():
                if pos == 2:  # 坤宫
                    sanqi_result[qi_name] = f"{qi_desc}临{gong}"
        
        return sanqi_result if sanqi_result else {"status": "三奇未入宫"}

    def get_jiuxing_info(self) -> List[str]:
        return JIUXING

    def get_bamen_info(self) -> List[str]:
        return BAMEN
