from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from ...persistence.database import get_db
from ...persistence.models.user import User
from ...core.dependencies import get_current_user, oauth2_scheme
from ...llm.llm_service import LLMService
from ...services.computation_service import ComputationService
from datetime import datetime

router = APIRouter()

class ChatRequest(BaseModel):
    message: str = Field(..., description="用户消息")
    domain: Optional[str] = Field(None, description="术数域")
    computation_result: Optional[Dict[str, Any]] = Field(None, description="计算结果")

class ChatResponse(BaseModel):
    message: str
    timestamp: str
    confidence: float

@router.post("/chat", response_model=ChatResponse, summary="命理聊天")
async def chat(
    request: ChatRequest,
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    llm_service = LLMService()
    
    try:
        if request.computation_result:
            explanation = await llm_service.explain_result(
                domain=request.domain or "八字",
                result=request.computation_result,
                user_question=request.message
            )
        else:
            explanation = await llm_service.explain_result(
                domain=request.domain or "八字",
                result={},
                user_question=request.message
            )
        
        return ChatResponse(
            message=explanation,
            timestamp=datetime.utcnow().isoformat(),
            confidence=0.85
        )
    
    except Exception as e:
        return ChatResponse(
            message=f"抱歉，我无法回答您的问题。错误：{str(e)}",
            timestamp=datetime.utcnow().isoformat(),
            confidence=0.0
        )

@router.post("/analyze", summary="综合分析")
async def analyze(
    birth_date: str,
    birth_time: str,
    timezone: str = "UTC+8",
    location: str = "",
    domains: Optional[list] = None,
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = None
    if token:
        user = await get_current_user(db, token)
    
    user_id = user.id if user else None
    computation_service = ComputationService(db)
    llm_service = LLMService()
    
    if not domains:
        domains = ["bazi", "ziwei"]
    
    results = []
    for domain in domains:
        try:
            result = computation_service.calculate(
                domain=domain,
                birth_date=datetime.strptime(birth_date, "%Y-%m-%d"),
                birth_time=birth_time,
                timezone=timezone,
                location=location,
                user_id=user_id
            )
            results.append({
                "domain": domain,
                "result": result
            })
        except Exception as e:
            results.append({
                "domain": domain,
                "error": str(e)
            })
    
    try:
        summary = await llm_service.summarize_analysis(results)
    except Exception as e:
        summary = f"LLM服务不可用: {str(e)}"
    
    return {
        "analyses": results,
        "summary": summary,
        "timestamp": datetime.utcnow().isoformat()
    }