
from datetime import datetime
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ...engines import BaziEngine, ZiweiEngine

router = APIRouter()

bazi_engine = BaziEngine()
ziwei_engine = ZiweiEngine()


class ComprehensiveRequest(BaseModel):
    name: Optional[str] = Field(None, description="姓名")
    birth_date: str = Field(..., description="出生日期 (YYYY-MM-DD)")
    birth_time: str = Field(..., description="出生时间 (HH:MM)")
    timezone: str = Field("UTC+8", description="时区")
    location: str = Field("", description="出生地点")
    domains: List[str] = Field(["bazi", "ziwei"], description="需要分析的术数域")


class ComprehensiveResponse(BaseModel):
    success: bool = Field(..., description="计算是否成功")
    results: Dict[str, Dict[str, Any]] = Field(..., description="各术数域计算结果")
    summary: str = Field("", description="综合分析摘要")
    confidence: float = Field(..., description="整体置信度")
    error: Optional[str] = Field(None, description="错误信息")


@router.post("/comprehensive", response_model=ComprehensiveResponse, summary="综合命理分析")
async def comprehensive_analysis(request: ComprehensiveRequest):
    try:
        birth_date = datetime.strptime(request.birth_date, "%Y-%m-%d")
        results = {}
        
        if "bazi" in request.domains:
            bazi_result = bazi_engine.calculate(birth_date, request.birth_time, request.timezone, request.location)
            if bazi_result.success:
                results["bazi"] = bazi_result.result
        
        if "ziwei" in request.domains:
            ziwei_result = ziwei_engine.calculate(birth_date, request.birth_time, request.timezone, request.location)
            if ziwei_result.success:
                results["ziwei"] = ziwei_result.result
        
        summary = _generate_summary(results)
        
        return {
            "success": len(results) > 0,
            "results": results,
            "summary": summary,
            "confidence": min([0.99, 0.95]) if results else 0.0,
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
        summaries.append(f"八字排盘: {bazi.get('bazi_pillar', '')}")
        summaries.append(f"日主: {bazi.get('daymaster', '')}")
        if "wuxing" in bazi:
            wuxing = bazi["wuxing"]
            max_element = max(wuxing, key=wuxing.get)
            summaries.append(f"五行偏旺: {max_element}")
    
    if "ziwei" in results:
        ziwei = results["ziwei"]
        summaries.append(f"紫微宫: {ziwei.get('ziwei_palace', '')}")
    
    return "; ".join(summaries)


@router.get("/domains", summary="获取支持的术数域")
async def get_supported_domains():
    return {
        "domains": [
            {"id": "bazi", "name": "八字", "description": "四柱八字命理分析"},
            {"id": "ziwei", "name": "紫微斗数", "description": "紫微斗数命理分析"},
            {"id": "qimen", "name": "奇门遁甲", "description": "奇门遁甲预测", "status": "coming_soon"},
            {"id": "liuren", "name": "大六壬", "description": "大六壬预测", "status": "coming_soon"},
            {"id": "meihua", "name": "梅花易数", "description": "梅花易数占卜", "status": "coming_soon"},
            {"id": "liuyao", "name": "六爻", "description": "六爻占卜", "status": "coming_soon"},
            {"id": "taiyi", "name": "太乙数", "description": "太乙神数", "status": "coming_soon"}
        ]
    }
