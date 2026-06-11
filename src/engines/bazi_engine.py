
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from .base_engine import BaseEngine, CalculationResult, ReasoningStep
from ..utils.calendar import convert_to_lunar, get_solar_term
from ..utils.bazi_utils import (
    TIANGAN, DIZHI, TIANGAN_WUXING, DIZHI_WUXING,
    TIANGAN_YINYANG, DIZHI_YINYANG, SHISEN,
    get_year_stem, get_month_stem, get_day_stem_branch, get_hour_stem,
    calculate_shishen, get_nayin
)
from ..utils.dayun_utils import (
    calculate_dayun, calculate_liunian, get_current_dayun, analyze_dayun_liunian
)


class BaziEngine(BaseEngine):
    DOMAIN: str = "bazi"

    def __init__(self, rules: Optional[Dict[str, Any]] = None):
        super().__init__(rules)
        self._load_rules()

    def _load_rules(self):
        if not self.rules:
            self.rules = {
                "version": "1.0.0",
                "source": "《渊海子平》《滴天髓》《穷通宝鉴》",
                "schools": ["月令派", "从旺派", "正官格"]
            }

    def calculate(self, birth_date: datetime, birth_time: str, 
                  timezone: str, location: str) -> CalculationResult:
        self.clear_reasoning_chain()
        
        try:
            lunar_date, solar_term = self._convert_to_lunar(birth_date)
            year_stem, year_branch = self._calculate_year_pillar(lunar_date)
            month_stem, month_branch = self._calculate_month_pillar(lunar_date, solar_term)
            day_stem, day_branch = self._calculate_day_pillar(birth_date)
            hour_stem, hour_branch = self._calculate_hour_pillar(birth_time, day_stem)
            
            bazi_pillar = f"{year_stem}{year_branch} {month_stem}{month_branch} {day_stem}{day_branch} {hour_stem}{hour_branch}"
            
            ten_gods = calculate_shishen(day_stem, [year_stem, month_stem, day_stem, hour_stem])
            
            nayin = {
                "year": get_nayin(year_stem, year_branch),
                "month": get_nayin(month_stem, month_branch),
                "day": get_nayin(day_stem, day_branch),
                "hour": get_nayin(hour_stem, hour_branch)
            }
            
            wuxing = self._calculate_wuxing([year_stem, month_stem, day_stem, hour_stem],
                                          [year_branch, month_branch, day_branch, hour_branch])
            
            result = {
                "bazi_pillar": bazi_pillar,
                "year": {"stem": year_stem, "branch": year_branch},
                "month": {"stem": month_stem, "branch": month_branch},
                "day": {"stem": day_stem, "branch": day_branch},
                "hour": {"stem": hour_stem, "branch": hour_branch},
                "daymaster": day_stem,
                "ten_gods": ten_gods,
                "nayin": nayin,
                "wuxing": wuxing,
                "solar_term": solar_term,
                "rules_version": self.rules.get("version", "1.0.0"),
                "school": self.rules.get("schools", ["月令派"])[0]
            }
            
            return CalculationResult(
                success=True,
                result=result,
                reasoning_chain=self.get_reasoning_chain(),
                confidence=0.99
            )
            
        except Exception as e:
            return CalculationResult(
                success=False,
                result={},
                reasoning_chain=self.get_reasoning_chain(),
                confidence=0.0,
                error=str(e)
            )

    def _convert_to_lunar(self, birth_date: datetime) -> Tuple[Dict[str, int], str]:
        lunar_date = convert_to_lunar(birth_date)
        solar_term = get_solar_term(birth_date)
        
        self.add_reasoning_step(
            rule_id="bazi.calendar.convert",
            description="公历转农历并获取节气",
            input_data={"solar_date": birth_date.isoformat()},
            output_data={"lunar_date": lunar_date, "solar_term": solar_term},
            confidence=1.0
        )
        
        return lunar_date, solar_term

    def _calculate_year_pillar(self, lunar_date: Dict[str, int]) -> Tuple[str, str]:
        year = lunar_date["year"]
        month = lunar_date["month"]
        day = lunar_date["day"]
        
        if month <= 2:
            year -= 1
        
        stem = get_year_stem(year)
        branch = DIZHI[(year - 4) % 12]
        
        self.add_reasoning_step(
            rule_id="bazi.pillar.year",
            description="计算年柱",
            input_data={"lunar_year": year, "lunar_month": month},
            output_data={"stem": stem, "branch": branch},
            confidence=1.0
        )
        
        return stem, branch

    def _calculate_month_pillar(self, lunar_date: Dict[str, int], solar_term: str) -> Tuple[str, str]:
        year_stem = get_year_stem(lunar_date["year"])
        month_idx = self._get_month_index(solar_term, lunar_date["month"])
        stem = get_month_stem(year_stem, month_idx)
        branch = DIZHI[(month_idx - 1) % 12]
        
        self.add_reasoning_step(
            rule_id="bazi.pillar.month",
            description="计算月柱",
            input_data={"year_stem": year_stem, "solar_term": solar_term, "lunar_month": lunar_date["month"]},
            output_data={"stem": stem, "branch": branch},
            confidence=1.0
        )
        
        return stem, branch

    def _get_month_index(self, solar_term: str, lunar_month: int) -> int:
        spring_terms = ["立春", "雨水"]
        if solar_term in spring_terms:
            return 1
        return lunar_month

    def _calculate_day_pillar(self, birth_date: datetime) -> Tuple[str, str]:
        stem, branch = get_day_stem_branch(birth_date)
        
        self.add_reasoning_step(
            rule_id="bazi.pillar.day",
            description="计算日柱",
            input_data={"solar_date": birth_date.isoformat()},
            output_data={"stem": stem, "branch": branch},
            confidence=1.0
        )
        
        return stem, branch

    def _calculate_hour_pillar(self, birth_time: str, day_stem: str) -> Tuple[str, str]:
        hour = int(birth_time.split(":")[0])
        minute = int(birth_time.split(":")[1]) if ":" in birth_time else 0
        
        if minute >= 30:
            hour += 1
        hour = hour % 24
        
        branch_idx = (hour + 1) // 2
        if branch_idx >= 12:
            branch_idx = 0
        branch = DIZHI[branch_idx]
        
        stem = get_hour_stem(day_stem, branch_idx)
        
        self.add_reasoning_step(
            rule_id="bazi.pillar.hour",
            description="计算时柱",
            input_data={"birth_time": birth_time, "day_stem": day_stem},
            output_data={"stem": stem, "branch": branch},
            confidence=1.0
        )
        
        return stem, branch

    def _calculate_wuxing(self, stems: list, branches: list) -> Dict[str, int]:
        wuxing_counts = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
        
        for stem in stems:
            if stem in TIANGAN_WUXING:
                wuxing_counts[TIANGAN_WUXING[stem]] += 1
        
        for branch in branches:
            if branch in DIZHI_WUXING:
                for wuxing, val in DIZHI_WUXING[branch].items():
                    wuxing_counts[wuxing] += val
        
        return wuxing_counts
    
    def calculate_dayun(self, birth_date: datetime, gender: str = "男") -> Dict[str, Any]:
        """
        计算大运
        
        Args:
            birth_date: 出生日期
            gender: 性别（"男"或"女"）
        
        Returns:
            大运计算结果
        """
        try:
            lunar_date, solar_term = self._convert_to_lunar(birth_date)
            year_stem, year_branch = self._calculate_year_pillar(lunar_date)
            month_stem, month_branch = self._calculate_month_pillar(lunar_date, solar_term)
            day_stem, day_branch = self._calculate_day_pillar(birth_date)
            
            dayun_result = calculate_dayun(
                daymaster=day_stem,
                month_stem=month_stem,
                month_branch=month_branch,
                gender=gender,
                birth_year=birth_date.year
            )
            
            self.add_reasoning_step(
                rule_id="bazi.dayun.calculate",
                description="计算大运",
                input_data={"daymaster": day_stem, "month": month_stem + month_branch, "gender": gender},
                output_data={"direction": dayun_result["direction"], "start_age": dayun_result["start_age"]},
                confidence=0.95
            )
            
            return {
                "success": True,
                "dayun": dayun_result,
                "reasoning_chain": [step.to_dict() for step in self.get_reasoning_chain()]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "dayun": {}
            }
    
    def calculate_liunian(self, birth_year: int, current_age: int, years: int = 10) -> Dict[str, Any]:
        """
        计算流年
        
        Args:
            birth_year: 出生年份
            current_age: 当前年龄
            years: 计算年数
        
        Returns:
            流年计算结果
        """
        try:
            liunian_list = calculate_liunian(birth_year, current_age, years)
            
            self.add_reasoning_step(
                rule_id="bazi.liunian.calculate",
                description="计算流年",
                input_data={"birth_year": birth_year, "current_age": current_age, "years": years},
                output_data={"liunian_count": len(liunian_list)},
                confidence=1.0
            )
            
            return {
                "success": True,
                "liunian": liunian_list,
                "reasoning_chain": [step.to_dict() for step in self.get_reasoning_chain()]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "liunian": []
            }
    
    def calculate_dayun_liunian(self, birth_date: datetime, gender: str = "男", 
                                current_age: int = 30) -> Dict[str, Any]:
        """
        综合计算大运流年
        
        Args:
            birth_date: 出生日期
            gender: 性别
            current_age: 当前年龄
        
        Returns:
            综合分析结果
        """
        try:
            # 计算大运
            dayun_result = self.calculate_dayun(birth_date, gender)
            
            # 计算流年
            liunian_result = self.calculate_liunian(birth_date.year, current_age, 10)
            
            # 获取当前大运
            current_dayun = get_current_dayun(
                dayun_result.get("dayun", {}).get("dayun_list", []),
                current_age
            )
            
            # 分析当前大运与流年关系
            analysis_list = []
            for liunian in liunian_result.get("liunian", []):
                daymaster = self.calculate(birth_date, "12:00", "UTC+8", "").result.get("daymaster", "")
                analysis = analyze_dayun_liunian(current_dayun, liunian, daymaster)
                analysis_list.append(analysis)
            
            return {
                "success": True,
                "dayun": dayun_result.get("dayun", {}),
                "liunian": liunian_result.get("liunian", []),
                "current_dayun": current_dayun,
                "analysis": analysis_list,
                "reasoning_chain": [step.to_dict() for step in self.get_reasoning_chain()]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
