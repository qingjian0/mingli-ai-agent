
from datetime import datetime
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ...engines import (
    BaziEngine, ZiweiEngine, QimenEngine, 
    LiurenEngine, MeihuaEngine, LiuyaoEngine, TaiyiEngine
)

router = APIRouter()

# 初始化所有7个术数引擎
engines = {
    "bazi": BaziEngine(),
    "ziwei": ZiweiEngine(),
    "qimen": QimenEngine(),
    "liuren": LiurenEngine(),
    "meihua": MeihuaEngine(),
    "liuyao": LiuyaoEngine(),
    "taiyi": TaiyiEngine()
}

# 术数域名称映射
domain_names = {
    "bazi": "八字",
    "ziwei": "紫微斗数",
    "qimen": "奇门遁甲",
    "liuren": "大六壬",
    "meihua": "梅花易数",
    "liuyao": "六爻",
    "taiyi": "太乙数"
}


class ComprehensiveRequest(BaseModel):
    name: Optional[str] = Field(None, description="姓名")
    birth_date: str = Field(..., description="出生日期 (YYYY-MM-DD)")
    birth_time: str = Field(..., description="出生时间 (HH:MM)")
    timezone: str = Field("UTC+8", description="时区")
    location: str = Field("", description="出生地点")
    domains: List[str] = Field(
        ["bazi", "ziwei", "qimen", "liuren", "meihua", "liuyao", "taiyi"], 
        description="需要分析的术数域"
    )


class ComprehensiveResponse(BaseModel):
    success: bool = Field(..., description="计算是否成功")
    results: Dict[str, Dict[str, Any]] = Field(..., description="各术数域计算结果")
    summary: str = Field("", description="综合分析摘要")
    confidence: float = Field(..., description="整体置信度")
    error: Optional[str] = Field(None, description="错误信息")


@router.post("/comprehensive", response_model=ComprehensiveResponse, summary="综合命理分析（支持全7大术数域）")
async def comprehensive_analysis(request: ComprehensiveRequest):
    try:
        birth_date = datetime.strptime(request.birth_date, "%Y-%m-%d")
        results = {}
        confidences = []
        
        # 遍历请求的所有术数域进行计算
        for domain in request.domains:
            if domain in engines:
                engine = engines[domain]
                result = engine.calculate(birth_date, request.birth_time, request.timezone, request.location)
                
                if result.success:
                    results[domain] = result.result
                    confidences.append(result.confidence)
        
        # 生成综合摘要
        summary = _generate_summary(results)
        
        # 计算整体置信度
        overall_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        return {
            "success": len(results) > 0,
            "results": results,
            "summary": summary,
            "confidence": overall_confidence,
            "error": None
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"日期格式错误: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算失败: {str(e)}")


def _generate_summary(results: Dict[str, Dict[str, Any]]) -> str:
    summaries = []
    
    if "bazi" in results:
        bazi = results["bazi"]
        summaries.append(f"【八字】排盘: {bazi.get('bazi_pillar', '')}")
        summaries.append(f"日主: {bazi.get('daymaster', '')}")
        if "wuxing" in bazi:
            wuxing = bazi["wuxing"]
            max_element = max(wuxing, key=wuxing.get)
            summaries.append(f"五行偏旺: {max_element}")
    
    if "ziwei" in results:
        ziwei = results["ziwei"]
        summaries.append(f"【紫微】宫: {ziwei.get('ziwei_palace', '')}")
    
    if "qimen" in results:
        qimen = results["qimen"]
        summaries.append(f"【奇门】盘: {qimen.get('pan_type', '')}")
    
    if "liuren" in results:
        liuren = results["liuren"]
        summaries.append(f"【六壬】月将: {liuren.get('yuejiang', '')}")
    
    if "meihua" in results:
        meihua = results["meihua"]
        shang = meihua.get("shang_gua", {}).get("name", "")
        xia = meihua.get("xia_gua", {}).get("name", "")
        summaries.append(f"【梅花】卦: {shang}{xia}")
    
    if "liuyao" in results:
        liuyao = results["liuyao"]
        gua = liuyao.get("gua", {}).get("name", "")
        summaries.append(f"【六爻】卦: {gua}")
    
    if "taiyi" in results:
        taiyi = results["taiyi"]
        summaries.append(f"【太乙】局数: {taiyi.get('jushu', '')}")
    
    return "; ".join(summaries)


@router.get("/domains", summary="获取支持的术数域")
async def get_supported_domains():
    return {
        "domains": [
            {"id": "bazi", "name": "八字", "description": "四柱八字命理分析", "status": "available"},
            {"id": "ziwei", "name": "紫微斗数", "description": "紫微斗数命理分析", "status": "available"},
            {"id": "qimen", "name": "奇门遁甲", "description": "奇门遁甲预测", "status": "available"},
            {"id": "liuren", "name": "大六壬", "description": "大六壬预测", "status": "available"},
            {"id": "meihua", "name": "梅花易数", "description": "梅花易数占卜", "status": "available"},
            {"id": "liuyao", "name": "六爻", "description": "六爻占卜", "status": "available"},
            {"id": "taiyi", "name": "太乙数", "description": "太乙神数", "status": "available"}
        ]
    }


@router.get("/status", summary="检查所有术数引擎状态")
async def check_engine_status():
    status = {}
    for domain, engine in engines.items():
        status[domain] = {
            "name": domain_names[domain],
            "status": "available",
            "version": engine.rules.get("version", "1.0.0"),
            "domain": engine.DOMAIN
        }
    return {"engines": status}
