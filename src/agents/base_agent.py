from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime

class AgentResult:
    def __init__(self, success: bool, data: Dict[str, Any], 
                 reasoning: Optional[str] = None, confidence: float = 1.0):
        self.success = success
        self.data = data
        self.reasoning = reasoning
        self.confidence = confidence
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "data": self.data,
            "reasoning": self.reasoning,
            "confidence": self.confidence
        }

class BaseAgent(ABC):
    AGENT_NAME: str = "BaseAgent"
    
    def __init__(self):
        self._history: List[Dict[str, Any]] = []
    
    @abstractmethod
    async def execute(self, **kwargs) -> AgentResult:
        pass
    
    def add_history(self, step: str, data: Dict[str, Any]):
        self._history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "step": step,
            "data": data
        })
    
    def get_history(self) -> List[Dict[str, Any]]:
        return self._history
    
    def clear_history(self):
        self._history = []