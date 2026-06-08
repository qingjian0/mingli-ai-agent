
from typing import Dict, List, Tuple
from .bazi_utils import TIANGAN, DIZHI, TIANGAN_YINYANG


def calculate_dayun(daymaster: str, month_stem: str, month_branch: str, 
                    gender: str = "男", birth_year: int = 2000) -> Dict[str, any]:
    """
    计算大运
    
    Args:
        daymaster: 日主（日干）
        month_stem: 月干
        month_branch: 月支
        gender: 性别（"男"或"女"）
        birth_year: 出生年份
    
    Returns:
        包含大运信息的字典
    """
    # 判断顺逆
    daymaster_yang = TIANGAN_YINYANG.get(daymaster, "阳") == "阳"
    
    # 阳男阴女顺行，阴男阳女逆行
    if (gender == "男" and daymaster_yang) or (gender == "女" and not daymaster_yang):
        direction = "顺行"
    else:
        direction = "逆行"
    
    # 计算起运年龄
    start_age = calculate_qiyun_age(month_stem, month_branch, direction)
    
    # 生成大运序列
    dayun_list = generate_dayun_sequence(month_stem, month_branch, direction, start_age)
    
    return {
        "direction": direction,
        "start_age": start_age,
        "dayun_list": dayun_list,
        "total_steps": len(dayun_list)
    }


def calculate_qiyun_age(month_stem: str, month_branch: str, direction: str) -> int:
    """
    计算起运年龄
    
    根据节气距离计算起运年龄，简化处理返回默认值
    """
    # 简化处理：默认起运年龄
    return 1


def generate_dayun_sequence(month_stem: str, month_branch: str, 
                           direction: str, start_age: int, 
                           steps: int = 8) -> List[Dict[str, any]]:
    """
    生成大运序列
    
    Args:
        month_stem: 月干
        month_branch: 月支
        direction: 方向（"顺行"或"逆行"）
        start_age: 起运年龄
        steps: 大运步数
    
    Returns:
        大运序列列表
    """
    dayun_list = []
    
    stem_idx = TIANGAN.index(month_stem)
    branch_idx = DIZHI.index(month_branch)
    
    step_direction = 1 if direction == "顺行" else -1
    
    for i in range(steps):
        new_stem_idx = (stem_idx + (i + 1) * step_direction) % 10
        new_branch_idx = (branch_idx + (i + 1) * step_direction) % 12
        
        age_start = start_age + i * 10
        age_end = age_start + 9
        
        dayun_list.append({
            "step": i + 1,
            "stem": TIANGAN[new_stem_idx],
            "branch": DIZHI[new_branch_idx],
            "ganzhi": TIANGAN[new_stem_idx] + DIZHI[new_branch_idx],
            "age_range": f"{age_start}-{age_end}",
            "age_start": age_start,
            "age_end": age_end
        })
    
    return dayun_list


def calculate_liunian(birth_year: int, current_age: int, years: int = 10) -> List[Dict[str, any]]:
    """
    计算流年
    
    Args:
        birth_year: 出生年份
        current_age: 当前年龄
        years: 计算年数
    
    Returns:
        流年序列列表
    """
    liunian_list = []
    
    for i in range(years):
        year = birth_year + current_age + i
        age = current_age + i
        
        # 计算年干支
        stem_idx = (year - 4) % 10
        branch_idx = (year - 4) % 12
        
        liunian_list.append({
            "year": year,
            "age": age,
            "stem": TIANGAN[stem_idx],
            "branch": DIZHI[branch_idx],
            "ganzhi": TIANGAN[stem_idx] + DIZHI[branch_idx]
        })
    
    return liunian_list


def get_current_dayun(dayun_list: List[Dict], current_age: int) -> Dict[str, any]:
    """
    获取当前大运
    
    Args:
        dayun_list: 大运列表
        current_age: 当前年龄
    
    Returns:
        当前大运信息
    """
    for dayun in dayun_list:
        if dayun["age_start"] <= current_age <= dayun["age_end"]:
            return dayun
    
    return dayun_list[0] if dayun_list else {}


def analyze_dayun_liunian(dayun: Dict, liunian: Dict, daymaster: str) -> Dict[str, any]:
    """
    分析大运流年关系
    
    Args:
        dayun: 大运信息
        liunian: 流年信息
        daymaster: 日主
    
    Returns:
        分析结果
    """
    from .bazi_utils import calculate_shishen
    
    # 计算大运十神
    dayun_shishen = calculate_shishen(daymaster, [dayun.get("stem", "")])
    
    # 计算流年十神
    liunian_shishen = calculate_shishen(daymaster, [liunian.get("stem", "")])
    
    return {
        "dayun_ganzhi": dayun.get("ganzhi", ""),
        "liunian_ganzhi": liunian.get("ganzhi", ""),
        "dayun_shishen": list(dayun_shishen.keys()) if dayun_shishen else [],
        "liunian_shishen": list(liunian_shishen.keys()) if liunian_shishen else [],
        "summary": f"大运{dayun.get('ganzhi', '')}，流年{liunian.get('ganzhi', '')}"
    }
