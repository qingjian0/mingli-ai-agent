from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from ..engines import BaziEngine, ZiweiEngine, QimenEngine, LiurenEngine, MeihuaEngine, LiuyaoEngine, TaiyiEngine
from ..persistence.models.computation import ComputationRequest, ComputationStep
from ..persistence.models.audit import AuditLog
from ..core.exceptions import CalculationException, NotFoundException
from ..config import settings

class ComputationService:
    ENGINES = {
        "bazi": BaziEngine,
        "ziwei": ZiweiEngine,
        "qimen": QimenEngine,
        "liuren": LiurenEngine,
        "meihua": MeihuaEngine,
        "liuyao": LiuyaoEngine,
        "taiyi": TaiyiEngine
    }
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate(self, domain: str, birth_date: datetime, birth_time: str, 
                  timezone: str = "UTC+8", location: str = "", user_id: Optional[int] = None) -> Dict[str, Any]:
        if domain not in self.ENGINES:
            raise CalculationException(message=f"不支持的术数域: {domain}")
        
        engine = self.ENGINES[domain]()
        
        try:
            result = engine.calculate(birth_date, birth_time, timezone, location)
            
            if user_id:
                self._save_computation(user_id, domain, {
                    "birth_date": birth_date.isoformat(),
                    "birth_time": birth_time,
                    "timezone": timezone,
                    "location": location
                }, result)
            
            return result.to_dict()
        
        except Exception as e:
            raise CalculationException(message=f"计算失败: {str(e)}")
    
    def _save_computation(self, user_id: int, domain: str, input_data: Dict[str, Any], result) -> None:
        request = ComputationRequest(
            user_id=user_id,
            domain=domain,
            status="completed" if result.success else "failed",
            input_data=input_data,
            result_data=result.result if result.success else {},
            confidence=result.confidence,
            error_message=result.error if not result.success else None,
            completed_at=datetime.utcnow()
        )
        
        self.db.add(request)
        self.db.commit()
        self.db.refresh(request)
        
        if result.reasoning_chain:
            for idx, step in enumerate(result.reasoning_chain):
                computation_step = ComputationStep(
                    request_id=request.id,
                    step_order=idx,
                    rule_id=step.rule_id,
                    description=step.description,
                    input_data=step.input_data,
                    output_data=step.output_data,
                    confidence=step.confidence
                )
                self.db.add(computation_step)
        
        self.db.commit()
    
    def get_computation_history(self, user_id: Optional[int] = None, domain: Optional[str] = None, 
                                limit: int = 20, offset: int = 0) -> list:
        query = self.db.query(ComputationRequest)
        
        if user_id:
            query = query.filter(ComputationRequest.user_id == user_id)
        
        if domain:
            query = query.filter(ComputationRequest.domain == domain)
        
        return query.order_by(ComputationRequest.created_at.desc()).offset(offset).limit(limit).all()
    
    def get_computation_by_id(self, computation_id: int, user_id: Optional[int] = None) -> ComputationRequest:
        query = self.db.query(ComputationRequest).filter(ComputationRequest.id == computation_id)
        
        if user_id:
            query = query.filter(ComputationRequest.user_id == user_id)
        
        computation = query.first()
        
        if not computation:
            raise NotFoundException(message="计算记录不存在")
        
        return computation
    
    def delete_computation(self, computation_id: int, user_id: Optional[int] = None):
        computation = self.get_computation_by_id(computation_id, user_id)
        self.db.delete(computation)
        self.db.commit()