
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ...engines import LiuyaoEngine

router = APIRouter()

engine = LiuyaoEngine()


class LiuyaoRequest(BaseModel):
    name: Optional[str] = Field(None, description="姓名")
    birth_date: str = Field(..., description="出生日期 (YYYY-MM-DD)")
    birth_time: str = Field(..., description="出生时间 (HH:MM)")
    timezone: str = Field("UTC+8", description="时区")
    location: str = Field("", description="出生地点")


class LiuyaoResponse(BaseModel):
    success: bool = Field(..., description="计算是否成功")
    result: Dict[str, Any] = Field(..., description="计算结果")
    reasoning_chain: list = Field(..., description="推理链")
    confidence: float = Field(..., description="置信度")
    error: Optional[str] = Field(None, description="错误信息")


@router.post("/calc", response_model=LiuyaoResponse, summary="六爻起卦")
async def calculate_liuyao(request: LiuyaoRequest):
    try:
        birth_date = datetime.strptime(request.birth_date, "%Y-%m-%d")
        result = engine.calculate(birth_date, request.birth_time, request.timezone, request.location)
        return result.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"日期格式错误: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算失败: {str(e)}")


@router.get("/liushen", summary="获取六神信息")
async def get_liushen():
    return {
        "liushen": engine.get_liuqi_info(),
        "count": len(engine.get_liuqi_info())
    }


@router.get("/liuqin", summary="获取六亲信息")
async def get_liuqin():
    return {
        "liuqin": engine.get_liuqin_info(),
        "count": len(engine.get_liuqin_info())
    }
