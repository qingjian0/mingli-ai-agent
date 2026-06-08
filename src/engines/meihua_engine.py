
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from .base_engine import BaseEngine, CalculationResult, ReasoningStep
from ..utils.bazi_utils import TIANGAN, DIZHI, TIANGAN_WUXING, DIZHI_WUXING


BAGUA = {
    0: {"name": "乾", "symbol": "☰", "gua": "三连", "wuxing": "金", "members": "父"},
    1: {"name": "兑", "symbol": "☱", "gua": "上缺", "wuxing": "金", "members": "少女"},
    2: {"name": "离", "symbol": "☲", "gua": "中虚", "wuxing": "火", "members": "中女"},
    3: {"name": "震", "symbol": "☳", "gua": "仰盂", "wuxing": "木", "members": "长男"},
    4: {"name": "巽", "symbol": "☴", "gua": "下断", "wuxing": "木", "members": "长女"},
    5: {"name": "坎", "symbol": "☵", "gua": "中满", "wuxing": "水", "members": "中男"},
    6: {"name": "艮", "symbol": "☶", "gua": "覆碗", "wuxing": "土", "members": "少男"},
    7: {"name": "坤", "symbol": "☷", "gua": "六断", "wuxing": "土", "members": "母"}
}

WUXING_XINGSHENG = {
    "木": {"生": "火", "克": "金", "被生": "水", "被克": "火"},
    "火": {"生": "土", "克": "水", "被生": "木", "被克": "金"},
    "土": {"生": "金", "克": "木", "被生": "火", "被克": "水"},
    "金": {"生": "水", "克": "火", "被生": "土", "被克": "木"},
    "水": {"生": "木", "克": "土", "被生": "金", "被克": "火"}
}

YI_GUA = ["乾", "兑", "离", "震", "巽", "坎", "艮", "坤"]


class MeihuaEngine(BaseEngine):
    DOMAIN: str = "meihua"

    def __init__(self, rules: Optional[Dict[str, Any]] = None):
        super().__init__(rules)
        self._load_rules()

    def _load_rules(self):
        if not self.rules:
            self.rules = {
                "version": "1.0.0",
                "source": "《梅花易数》",
                "schools": ["经典分类法", "现代应用"]
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
            
            total = year + month + day + hour + minute
            
            shang_gua = self._calculate_gua(total, "上卦")
            
            self.add_reasoning_step(
                rule_id="meihua.shang_gua",
                description="计算上卦",
                input_data={"year": year, "month": month, "day": day, "hour": hour, "minute": minute},
                output_data={"total": total, "shang_gua": shang_gua},
                confidence=1.0
            )
            
            total_with_minute = total + minute
            xia_gua = self._calculate_gua(total_with_minute, "下卦")
            
            self.add_reasoning_step(
                rule_id="meihua.xia_gua",
                description="计算下卦",
                input_data={"total_with_minute": total_with_minute},
                output_data={"xia_gua": xia_gua},
                confidence=1.0
            )
            
            dong_yao = self._calculate_dongyao(total_with_minute)
            
            self.add_reasoning_step(
                rule_id="meihua.dong_yao",
                description="计算动爻",
                input_data={"total_with_minute": total_with_minute},
                output_data={"dong_yao": dong_yao},
                confidence=0.98
            )
            
            ti_yong = self._analyze_ti_yong(shang_gua, xia_gua)
            
            self.add_reasoning_step(
                rule_id="meihua.ti_yong",
                description="分析体用关系",
                input_data={"shang_gua": shang_gua, "xia_gua": xia_gua},
                output_data={"ti_yong": ti_yong},
                confidence=0.95
            )
            
            result = {
                "year": year,
                "month": month,
                "day": day,
                "hour": hour,
                "minute": minute,
                "shang_gua": shang_gua,
                "xia_gua": xia_gua,
                "dong_yao": dong_yao,
                "ti_yong": ti_yong,
                "rules_version": self.rules.get("version", "1.0.0"),
                "school": self.rules.get("schools", ["经典分类法"])[0]
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

    def _calculate_gua(self, total: int, gua_type: str) -> Dict[str, Any]:
        remainder = total % 8
        remainder = remainder if remainder > 0 else 8
        
        gua = BAGUA.get(remainder - 1, BAGUA[0])
        
        return {
            "index": remainder,
            "name": gua["name"],
            "symbol": gua["symbol"],
            "description": gua["gua"],
            "wuxing": gua["wuxing"],
            "members": gua["members"]
        }

    def _calculate_dongyao(self, total: int) -> int:
        remainder = total % 6
        return remainder if remainder > 0 else 6

    def _analyze_ti_yong(self, shang_gua: Dict, xia_gua: Dict) -> Dict[str, Any]:
        ti_wuxing = shang_gua["wuxing"]
        yong_wuxing = xia_gua["wuxing"]
        
        if ti_wuxing == yong_wuxing:
            relation = "比和"
            description = "体用比和，大吉，诸事顺遂"
            favorability = "大吉"
        elif WUXING_XINGSHENG.get(ti_wuxing, {}).get("被克") == yong_wuxing:
            relation = "体克用"
            description = "体克用，小吉，先难后易"
            favorability = "小吉"
        elif WUXING_XINGSHENG.get(ti_wuxing, {}).get("生") == yong_wuxing:
            relation = "体生用"
            description = "体生用，耗泄，宜守成"
            favorability = "中平"
        elif WUXING_XINGSHENG.get(yong_wuxing, {}).get("克") == ti_wuxing:
            relation = "用克体"
            description = "用克体，大凶，须防灾害"
            favorability = "大凶"
        elif WUXING_XINGSHENG.get(ti_wuxing, {}).get("被生") == yong_wuxing:
            relation = "体被生"
            description = "体被生，得助力，事半功倍"
            favorability = "吉"
        else:
            relation = "用生物"
            description = "用生物，耗体吉"
            favorability = "小吉"
        
        return {
            "ti": {"gua": shang_gua["name"], "wuxing": ti_wuxing},
            "yong": {"gua": xia_gua["name"], "wuxing": yong_wuxing},
            "relation": relation,
            "description": description,
            "favorability": favorability
        }

    def get_bagua_info(self) -> List[Dict[str, Any]]:
        return list(BAGUA.values())

    def interpret_gua(self, gua_name: str) -> Optional[Dict[str, Any]]:
        for idx, gua in BAGUA.items():
            if gua["name"] == gua_name:
                return gua
        return None
