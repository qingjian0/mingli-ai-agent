
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ...engines import ZiweiEngine

router = APIRouter()

engine = ZiweiEngine()


class ZiweiRequest(BaseModel):
    name: Optional[str] = Field(None, description="姓名")
    birth_date: str = Field(..., description="出生日期 (YYYY-MM-DD)")
    birth_time: str = Field(..., description="出生时间 (HH:MM)")
    timezone: str = Field("UTC+8", description="时区")
    location: str = Field("", description="出生地点")


class ZiweiResponse(BaseModel):
    success: bool = Field(..., description="计算是否成功")
    result: Dict[str, Any] = Field(..., description="计算结果")
    reasoning_chain: list = Field(..., description="推理链")
    confidence: float = Field(..., description="置信度")
    error: Optional[str] = Field(None, description="错误信息")


@router.post("/calc", response_model=ZiweiResponse, summary="紫微斗数排盘")
async def calculate_ziwei(request: ZiweiRequest):
    try:
        birth_date = datetime.strptime(request.birth_date, "%Y-%m-%d")
        result = engine.calculate(birth_date, request.birth_time, request.timezone, request.location)
        return result.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"日期格式错误: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算失败: {str(e)}")


@router.get("/stars", summary="获取紫微主星列表")
async def get_ziwei_stars():
    return {
        "main_stars": engine.get_main_stars(),
        "count": len(engine.get_main_stars())
    }


@router.get("/palaces", summary="获取十二宫信息")
async def get_ziwei_palaces():
    from ...utils.ziwei_utils import PALACES
    return PALACES
