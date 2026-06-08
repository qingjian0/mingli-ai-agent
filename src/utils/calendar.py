
from datetime import datetime
from typing import Dict, Optional
import lunardate


SOLAR_TERMS = [
    "小寒", "大寒", "立春", "雨水", "惊蛰", "春分",
    "清明", "谷雨", "立夏", "小满", "芒种", "夏至",
    "小暑", "大暑", "立秋", "处暑", "白露", "秋分",
    "寒露", "霜降", "立冬", "小雪", "大雪", "冬至"
]


def convert_to_lunar(solar_date: datetime) -> Dict[str, int]:
    lunar = lunardate.LunarDate.fromSolarDate(
        solar_date.year, solar_date.month, solar_date.day
    )
    return {
        "year": lunar.year,
        "month": lunar.month,
        "day": lunar.day,
        "is_leap": False
    }


def lunar_to_solar(lunar_year: int, lunar_month: int, lunar_day: int, is_leap: bool = False) -> datetime:
    lunar = lunardate.LunarDate(lunar_year, lunar_month, lunar_day, is_leap)
    solar = lunar.toSolarDate()
    return datetime(solar.year, solar.month, solar.day)


def get_solar_term(solar_date: datetime) -> str:
    ephemeris_data = _calculate_ephemeris(solar_date)
    return ephemeris_data.get("solar_term", "")


def _calculate_ephemeris(solar_date: datetime) -> Dict[str, str]:
    day_of_year = solar_date.timetuple().tm_yday
    term_index = int((day_of_year * 24) / 365.25)
    term_index = min(max(0, term_index), 23)
    
    return {
        "solar_term": SOLAR_TERMS[term_index],
        "day_of_year": day_of_year
    }


def get_jieqi_date(year: int, jieqi_name: str) -> Optional[datetime]:
    if jieqi_name not in SOLAR_TERMS:
        return None
    
    term_index = SOLAR_TERMS.index(jieqi_name)
    approximate_day = int((term_index + 0.5) * 365.25 / 24)
    
    try:
        return datetime(year, 1, 1).replace(day=1) + timedelta(days=approximate_day - 1)
    except:
        return None
