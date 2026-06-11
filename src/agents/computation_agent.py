from typing import Dict, Any, Optional
from datetime import datetime
from .base_agent import BaseAgent, AgentResult
from ..services.computation_service import ComputationService

class ComputationAgent(BaseAgent):
    AGENT_NAME: str = "ComputationAgent"
    
    def __init__(self, db_session):
        super().__init__()
        self.computation_service = ComputationService(db_session)
    
    async def execute(self, domain: str, birth_date: str, birth_time: str, 
                      timezone: str = "UTC+8", location: str = "", 
                      user_id: Optional[int] = None) -> AgentResult:
        self.add_history("start", {"domain": domain, "birth_date": birth_date})
        
        try:
            birth_date_dt = datetime.strptime(birth_date, "%Y-%m-%d")
            
            result = self.computation_service.calculate(
                domain=domain,
                birth_date=birth_date_dt,
                birth_time=birth_time,
                timezone=timezone,
                location=location,
                user_id=user_id
            )
            
            self.add_history("completed", {"success": result.get("success", False)})
            
            return AgentResult(
                success=result.get("success", False),
                data=result.get("result", {}),
                reasoning="术数计算完成",
                confidence=result.get("confidence", 0.0)
            )
        
        except Exception as e:
            self.add_history("error", {"message": str(e)})
            return AgentResult(
                success=False,
                data={},
                reasoning=f"计算失败: {str(e)}",
                confidence=0.0
            )