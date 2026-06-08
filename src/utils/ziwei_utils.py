
from typing import Dict, List, Tuple

PALACES = {
    "命宫": {"position": 0, "description": "生命核心"},
    "兄弟": {"position": 1, "description": "兄弟姐妹关系"},
    "夫妻": {"position": 2, "description": "婚姻感情"},
    "子女": {"position": 3, "description": "子女后代"},
    "财帛": {"position": 4, "description": "财富积累"},
    "疾厄": {"position": 5, "description": "健康状况"},
    "迁移": {"position": 6, "description": "外出旅行"},
    "交友": {"position": 7, "description": "朋友社交"},
    "事业": {"position": 8, "description": "工作事业"},
    "田宅": {"position": 9, "description": "房产资产"},
    "福德": {"position": 10, "description": "福分德行"},
    "父母": {"position": 11, "description": "父母长辈"}
}

STARS = {
    "main": [
        {"name": "紫微", "type": "emperor", "element": "土"},
        {"name": "天机", "type": "mercurial", "element": "木"},
        {"name": "太阳", "type": "yang", "element": "火"},
        {"name": "武曲", "type": "martial", "element": "金"},
        {"name": "天同", "type": "benevolent", "element": "水"},
        {"name": "廉贞", "type": "righteous", "element": "火"},
        {"name": "天府", "type": "treasury", "element": "土"},
        {"name": "太阴", "type": "yin", "element": "水"},
        {"name": "贪狼", "type": "greedy", "element": "木"},
        {"name": "巨门", "type": "door", "element": "土"},
        {"name": "天相", "type": "minister", "element": "水"},
        {"name": "天梁", "type": "beam", "element": "土"},
        {"name": "七杀", "type": "killer", "element": "金"},
        {"name": "破军", "type": "breaker", "element": "水"}
    ],
    "auxiliary": [
        {"name": "左辅", "type": "assistant"},
        {"name": "右弼", "type": "assistant"},
        {"name": "文昌", "type": "literary"},
        {"name": "文曲", "type": "literary"},
        {"name": "天魁", "type": "honor"},
        {"name": "天钺", "type": "honor"}
    ],
    "lukewarm": [
        {"name": "禄存", "type": "wealth"},
        {"name": "天马", "type": "travel"},
        {"name": "截空", "type": "void"},
        {"name": "旬空", "type": "void"}
    ],
    "four_horsemen": [
        {"name": "擎羊", "type": "evil"},
        {"name": "陀罗", "type": "evil"},
        {"name": "火星", "type": "evil"},
        {"name": "铃星", "type": "evil"}
    ],
    "others": [
        {"name": "天刑", "type": "punishment"},
        {"name": "天姚", "type": "romance"},
        {"name": "阴煞", "type": "dark"},
        {"name": "天哭", "type": "mourning"},
        {"name": "天虚", "type": "void"}
    ]
}


def get_ziwei_palace(lunar_year: int, lunar_month: int, lunar_day: int, birth_time: str) -> int:
    hour = int(birth_time.split(":")[0])
    base_num = (lunar_month * 30 + lunar_day + hour) % 12
    return base_num


def calculate_palace_positions(ziwei_position: int) -> Dict[str, int]:
    positions = {}
    palace_names = list(PALACES.keys())
    
    for i, palace_name in enumerate(palace_names):
        positions[palace_name] = (ziwei_position + i) % 12
    
    return positions


def get_stars_by_birth(lunar_year: int, birth_time: str) -> List[Dict[str, str]]:
    year_stem_branch = _get_year_stem_branch(lunar_year)
    hour_branch = _get_hour_branch(birth_time)
    
    stars = []
    
    for star in STARS["main"]:
        if _should_include_star(star, year_stem_branch, hour_branch):
            stars.append({
                "name": star["name"],
                "type": star["type"],
                "element": star.get("element", ""),
                "source": "main"
            })
    
    for star in STARS["auxiliary"]:
        stars.append({
            "name": star["name"],
            "type": star["type"],
            "source": "auxiliary"
        })
    
    for star in STARS["four_horsemen"]:
        stars.append({
            "name": star["name"],
            "type": star["type"],
            "source": "four_horsemen"
        })
    
    return stars


def _get_year_stem_branch(year: int) -> str:
    TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    return TIANGAN[(year - 4) % 10] + DIZHI[(year - 4) % 12]


def _get_hour_branch(birth_time: str) -> str:
    DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    hour = int(birth_time.split(":")[0])
    branch_idx = (hour + 1) // 2 % 12
    return DIZHI[branch_idx]


def _should_include_star(star: Dict[str, str], year_stem_branch: str, hour_branch: str) -> bool:
    main_star_rules = {
        "紫微": lambda y, h: True,
        "天机": lambda y, h: True,
        "太阳": lambda y, h: True,
        "武曲": lambda y, h: True,
        "天同": lambda y, h: True,
        "廉贞": lambda y, h: True,
        "天府": lambda y, h: True,
        "太阴": lambda y, h: True,
        "贪狼": lambda y, h: True,
        "巨门": lambda y, h: True,
        "天相": lambda y, h: True,
        "天梁": lambda y, h: True,
        "七杀": lambda y, h: True,
        "破军": lambda y, h: True
    }
    
    rule = main_star_rules.get(star["name"])
    return rule(year_stem_branch, hour_branch) if rule else True


def analyze_stars_in_palace(palace_position: int, stars: List[Dict[str, str]]) -> Dict[str, Any]:
    palace_stars = _get_stars_at_position(palace_position, stars)
    analysis = {
        "stars": palace_stars,
        "main_stars": [s for s in palace_stars if s["source"] == "main"],
        "auxiliary_stars": [s for s in palace_stars if s["source"] == "auxiliary"],
        "evil_stars": [s for s in palace_stars if s["source"] == "four_horsemen"],
        "interpretation": _generate_interpretation(palace_stars)
    }
    return analysis


def _get_stars_at_position(position: int, stars: List[Dict[str, str]]) -> List[Dict[str, str]]:
    selected_stars = []
    star_positions = {
        "紫微": 0, "天机": 1, "太阳": 2, "武曲": 3, "天同": 4, "廉贞": 5,
        "天府": 6, "太阴": 7, "贪狼": 8, "巨门": 9, "天相": 10, "天梁": 11,
        "七杀": 0, "破军": 1
    }
    
    for star in stars:
        if star["name"] in star_positions:
            if star_positions[star["name"]] == position:
                selected_stars.append(star)
    
    return selected_stars


def _generate_interpretation(stars: List[Dict[str, str]]) -> str:
    main_names = [s["name"] for s in stars if s["source"] == "main"]
    
    if not main_names:
        return "此宫无主星"
    
    interpretation_map = {
        "紫微": "紫微独坐，尊贵之相，领导力强",
        "天机": "天机入命，聪慧机敏，思维活跃",
        "太阳": "太阳高照，光明磊落，热心公益",
        "武曲": "武曲守命，刚毅果断，事业心重",
        "天同": "天同入命，性格温和，享受生活",
        "廉贞": "廉贞坐守，性情刚烈，办事公正",
        "天府": "天府入命，衣食丰足，稳重可靠",
        "太阴": "太阴入命，温柔细腻，艺术天赋",
        "贪狼": "贪狼入命，多才多艺，交际广泛",
        "巨门": "巨门坐守，言辞犀利，善于辩论",
        "天相": "天相入命，相貌端正，处事周全",
        "天梁": "天梁入命，乐于助人，有长辈缘",
        "七杀": "七杀坐守，性格刚强，决断力强",
        "破军": "破军入命，敢于革新，变动较多"
    }
    
    interpretations = [interpretation_map.get(name, f"{name}入命") for name in main_names]
    return "; ".join(interpretations)
