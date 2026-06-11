
from datetime import datetime
from typing import Dict, Any, Optional, List
from .base_engine import BaseEngine, CalculationResult, ReasoningStep
from ..utils.bazi_utils import GANZHI_HOURS


LIUQI_BASHEN = ["青龙", "朱雀", "勾陈", "螣蛇", "白虎", "玄武"]

LIUQIN = ["父母", "兄弟", "子孙", "妻财", "官鬼"]

SHI_YING_MAP = {
    "子": "世", "丑": "应",
    "寅": "世", "卯": "应",
    "辰": "世", "巳": "应",
    "午": "世", "未": "应",
    "申": "世", "酉": "应",
    "戌": "世", "亥": "应"
}


class LiuyaoEngine(BaseEngine):
    DOMAIN: str = "liuyao"

    def __init__(self, rules: Optional[Dict[str, Any]] = None):
        super().__init__(rules)
        self._load_rules()

    def _load_rules(self):
        if not self.rules:
            self.rules = {
                "version": "1.0.0",
                "source": "《周易》《六爻占筮详解》",
                "schools": ["动爻派", "变爻派", "日月建派"]
            }

    def calculate(self, birth_date: datetime, birth_time: str, 
                  timezone: str, location: str) -> CalculationResult:
        self.clear_reasoning_chain()
        
        try:
            year = birth_date.year
            month = birth_date.month
            day = birth_date.day
            
            hour = int(birth_time.split(":")[0])
            minute = int(birth_time.split(":")[1]) if ":" in birth_time else 0
            
            ri_ganzhi = self._get_ri_ganzhi(birth_date)
            
            self.add_reasoning_step(
                rule_id="liuyao.ri_ganzhi",
                description="获取日干支",
                input_data={"birth_date": birth_date.isoformat()},
                output_data={"ri_ganzhi": ri_ganzhi},
                confidence=1.0
            )
            
            ri_zhi = ri_ganzhi[-1]
            ri_gan = ri_ganzhi[0]
            
            shichen = self._get_shichen(birth_time)
            
            self.add_reasoning_step(
                rule_id="liuyao.shichen",
                description="获取时辰地支",
                input_data={"birth_time": birth_time},
                output_data={"shichen": shichen},
                confidence=1.0
            )
            
            yuejian = self._get_yuejian(month)
            
            self.add_reasoning_step(
                rule_id="liuyao.yuejian",
                description="确定月建",
                input_data={"month": month},
                output_data={"yuejian": yuejian},
                confidence=1.0
            )
            
            gua = self._calculate_gua(year, month, day, hour)
            
            self.add_reasoning_step(
                rule_id="liuyao.gua",
                description="起卦",
                input_data={"year": year, "month": month, "day": day, "hour": hour},
                output_data={"gua": gua},
                confidence=0.98
            )
            
            liuqin = self._assign_liuqin(ri_gan, gua)
            
            self.add_reasoning_step(
                rule_id="liuyao.liuqin",
                description="六亲分配",
                input_data={"ri_gan": ri_gan},
                output_data={"liuqin": liuqin},
                confidence=0.95
            )
            
            liushen = self._assign_liushen(gua)
            
            self.add_reasoning_step(
                rule_id="liuyao.liushen",
                description="六神分配",
                input_data={"gua": gua},
                output_data={"liushen": liushen},
                confidence=0.95
            )
            
            result = {
                "year": year,
                "month": month,
                "day": day,
                "hour": hour,
                "ri_ganzhi": ri_ganzhi,
                "shichen": shichen,
                "yuejian": yuejian,
                "gua": gua,
                "liuqin": liuqin,
                "liushen": liushen,
                "rules_version": self.rules.get("version", "1.0.0"),
                "school": self.rules.get("schools", ["动爻派"])[0]
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

    def _get_ri_ganzhi(self, birth_date: datetime) -> str:
        base_date = datetime(1900, 1, 1)
        days = (birth_date.date() - base_date.date()).days
        ganzhi_index = (days + 6) % 60
        return GANZHI_HOURS[ganzhi_index]

    def _get_shichen(self, birth_time: str) -> str:
        hour = int(birth_time.split(":")[0])
        shichen_list = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        return shichen_list[(hour + 1) // 2 % 12]

    def _get_yuejian(self, month: int) -> str:
        yuejian_list = ["寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"]
        return yuejian_list[month - 1]

    def _calculate_gua(self, year: int, month: int, day: int, hour: int) -> Dict[str, Any]:
        total = year + month + day + hour
        shang = (total // 4) % 8
        xia = ((total // 4) + (total % 4)) % 8
        
        shang = shang if shang > 0 else 8
        xia = xia if xia > 0 else 8
        
        hexagram = {
            "shang_gua": shang,
            "xia_gua": xia,
            "name": self._get_hexagram_name(shang, xia)
        }
        
        return hexagram

    def _get_hexagram_name(self, shang: int, xia: int) -> str:
        bagua = ["乾", "兑", "离", "震", "巽", "坎", "艮", "坤"]
        return bagua[shang - 1] + bagua[xia - 1]

    def _assign_liuqin(self, ri_gan: str, gua: Dict) -> Dict[str, str]:
        ri_gan_wuxing = {
            "甲": "木", "乙": "木", "丙": "火", "丁": "火",
            "戊": "土", "己": "土", "庚": "金", "辛": "金",
            "壬": "水", "癸": "水"
        }
        
        ri_wuxing = ri_gan_wuxing.get(ri_gan, "土")
        
        wuxing_order = ["木", "火", "土", "金", "水"]
        ri_idx = wuxing_order.index(ri_wuxing)
        
        liuqin_map = {}
        for i in range(6):
            wuxing_idx = (ri_idx + i) % 5
            liuqin_map[6 - i] = LIUQIN[wuxing_idx]
        
        return liuqin_map

    def _assign_liushen(self, gua: Dict) -> Dict[str, str]:
        shang = gua.get("shang_gua", 1)
        shen_start = (shang - 1) % 6
        
        liushen_map = {}
        for i in range(6):
            liushen_map[6 - i] = LIUQI_BASHEN[(shen_start + i) % 6]
        
        return liushen_map

    def get_liuqi_info(self) -> List[str]:
        return LIUQI_BASHEN

    def get_liuqin_info(self) -> List[str]:
        return LIUQIN
