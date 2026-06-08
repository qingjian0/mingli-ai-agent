
from typing import Dict, List, Tuple

TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

TIANGAN_WUXING = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水"
}

DIZHI_WUXING = {
    "子": {"水": 1},
    "丑": {"土": 1, "金": 0.3, "水": 0.2},
    "寅": {"木": 1, "火": 0.3, "土": 0.2},
    "卯": {"木": 1},
    "辰": {"土": 1, "水": 0.3, "木": 0.2},
    "巳": {"火": 1, "土": 0.3, "金": 0.2},
    "午": {"火": 1, "土": 0.3},
    "未": {"土": 1, "火": 0.3, "木": 0.2},
    "申": {"金": 1, "水": 0.3, "土": 0.2},
    "酉": {"金": 1},
    "戌": {"土": 1, "火": 0.3, "金": 0.2},
    "亥": {"水": 1, "木": 0.3}
}

TIANGAN_YINYANG = {
    "甲": "阳", "乙": "阴",
    "丙": "阳", "丁": "阴",
    "戊": "阳", "己": "阴",
    "庚": "阳", "辛": "阴",
    "壬": "阳", "癸": "阴"
}

DIZHI_YINYANG = {
    "子": "阳", "丑": "阴",
    "寅": "阳", "卯": "阴",
    "辰": "阳", "巳": "阴",
    "午": "阳", "未": "阴",
    "申": "阳", "酉": "阴",
    "戌": "阳", "亥": "阴"
}

SHISEN = ["比肩", "劫财", "食神", "伤官", "偏财", "正财", "七杀", "正官", "偏印", "正印"]


def get_year_stem(year: int) -> str:
    return TIANGAN[(year - 4) % 10]


def get_month_stem(year_stem: str, month_index: int) -> str:
    tiangan_index = TIANGAN.index(year_stem)
    
    wuhu_map = {
        "甲": 2, "己": 2,
        "乙": 4, "庚": 4,
        "丙": 6, "辛": 6,
        "丁": 8, "壬": 8,
        "戊": 0, "癸": 0
    }
    base_index = wuhu_map.get(year_stem, 2)
    
    month_stem_indices = [
        (base_index + 0) % 10,
        (base_index + 2) % 10,
        (base_index + 4) % 10,
        (base_index + 6) % 10,
        (base_index + 8) % 10,
        (base_index + 1) % 10,
        (base_index + 3) % 10,
        (base_index + 5) % 10,
        (base_index + 7) % 10,
        (base_index + 9) % 10,
        (base_index + 1) % 10,
        (base_index + 3) % 10
    ]
    return TIANGAN[month_stem_indices[month_index - 1]]


def get_day_stem_branch(solar_date) -> Tuple[str, str]:
    base_date = __import__('datetime').datetime(1900, 1, 1)
    delta_days = (solar_date - base_date).days
    
    stem_index = (delta_days + 9) % 10
    branch_index = (delta_days + 1) % 12
    
    return TIANGAN[stem_index], DIZHI[branch_index]


def get_hour_stem(day_stem: str, hour_branch_index: int) -> str:
    wushu_map = {
        "甲": 0, "己": 0,
        "乙": 2, "庚": 2,
        "丙": 4, "辛": 4,
        "丁": 6, "壬": 6,
        "戊": 8, "癸": 8
    }
    base_index = wushu_map.get(day_stem, 0)
    
    hour_stem_indices = [
        (base_index + 0) % 10,
        (base_index + 2) % 10,
        (base_index + 4) % 10,
        (base_index + 6) % 10,
        (base_index + 8) % 10,
        (base_index + 1) % 10,
        (base_index + 3) % 10,
        (base_index + 5) % 10,
        (base_index + 7) % 10,
        (base_index + 9) % 10,
        (base_index + 0) % 10,
        (base_index + 2) % 10
    ]
    return TIANGAN[hour_stem_indices[hour_branch_index]]


def calculate_shishen(daymaster: str, other_stems: List[str]) -> Dict[str, List[str]]:
    daymaster_index = TIANGAN.index(daymaster)
    shishen_map = {}
    
    for stem in other_stems:
        stem_index = TIANGAN.index(stem)
        diff = (stem_index - daymaster_index) % 10
        
        shishen_type = SHISEN[diff]
        if shishen_type not in shishen_map:
            shishen_map[shishen_type] = []
        shishen_map[shishen_type].append(stem)
    
    return shishen_map


NAYIN_MAP = {
    "甲子": "海中金", "乙丑": "海中金",
    "丙寅": "炉中火", "丁卯": "炉中火",
    "戊辰": "大林木", "己巳": "大林木",
    "庚午": "路旁土", "辛未": "路旁土",
    "壬申": "剑锋金", "癸酉": "剑锋金",
    "甲戌": "山头火", "乙亥": "山头火",
    "丙子": "涧下水", "丁丑": "涧下水",
    "戊寅": "城头土", "己卯": "城头土",
    "庚辰": "白蜡金", "辛巳": "白蜡金",
    "壬午": "杨柳木", "癸未": "杨柳木",
    "甲申": "泉中水", "乙酉": "泉中水",
    "丙戌": "屋上土", "丁亥": "屋上土",
    "戊子": "霹雳火", "己丑": "霹雳火",
    "庚寅": "松柏木", "辛卯": "松柏木",
    "壬辰": "长流水", "癸巳": "长流水",
    "甲午": "沙中金", "乙未": "沙中金",
    "丙申": "山下火", "丁酉": "山下火",
    "戊戌": "平地木", "己亥": "平地木",
    "庚子": "壁上土", "辛丑": "壁上土",
    "壬寅": "金箔金", "癸卯": "金箔金",
    "甲辰": "覆灯火", "乙巳": "覆灯火",
    "丙午": "天河水", "丁未": "天河水",
    "戊申": "大驿土", "己酉": "大驿土",
    "庚戌": "钗钏金", "辛亥": "钗钏金",
    "壬子": "桑柘木", "癸丑": "桑柘木",
    "甲寅": "大溪水", "乙卯": "大溪水",
    "丙辰": "沙中土", "丁巳": "沙中土",
    "戊午": "天上火", "己未": "天上火",
    "庚申": "石榴木", "辛酉": "石榴木",
    "壬戌": "大海水", "癸亥": "大海水"
}


def get_nayin(stem: str, branch: str) -> str:
    return NAYIN_MAP.get(stem + branch, "")
