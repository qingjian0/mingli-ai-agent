
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ...engines import QimenEngine

router = APIRouter()

engine = QimenEngine()


class QimenRequest(BaseModel):
    name: Optional[str] = Field(None, description="姓名")
    birth_date: str = Field(..., description="出生日期 (YYYY-MM-DD)")
    birth_time: str = Field(..., description="出生时间 (HH:MM)")
    timezone: str = Field("UTC+8", description="时区")
    location: str = Field("", description="出生地点")


class QimenResponse(BaseModel):
    success: bool = Field(..., description="计算是否成功")
    result: Dict[str, Any] = Field(..., description="计算结果")
    reasoning_chain: list = Field(..., description="推理链")
    confidence: float = Field(..., description="置信度")
    error: Optional[str] = Field(None, description="错误信息")


@router.post("/calc", response_model=QimenResponse, summary="奇门遁甲排盘")
async def calculate_qimen(request: QimenRequest):
    try:
        birth_date = datetime.strptime(request.birth_date, "%Y-%m-%d")
        result = engine.calculate(birth_date, request.birth_time, request.timezone, request.location)
        return result.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"日期格式错误: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算失败: {str(e)}")


@router.get("/jiuxing", summary="获取九星信息")
async def get_jiuxing():
    return {
        "stars": engine.get_jiuxing_info(),
        "count": len(engine.get_jiuxing_info())
    }


@router.get("/bamen", summary="获取八门信息")
async def get_bamen():
    return {
        "doors": engine.get_bamen_info(),
        "count": len(engine.get_bamen_info())
    }
