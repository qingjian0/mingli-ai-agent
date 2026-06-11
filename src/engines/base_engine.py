
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime


class ReasoningStep:
    def __init__(self, rule_id: str, description: str, input_data: Dict[str, Any], 
                 output_data: Dict[str, Any], confidence: float = 1.0):
        self.rule_id = rule_id
        self.description = description
        self.input_data = input_data
        self.output_data = output_data
        self.confidence = confidence

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "description": self.description,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "confidence": self.confidence
        }


class CalculationResult:
    def __init__(self, success: bool, result: Dict[str, Any], 
                 reasoning_chain: List[ReasoningStep], 
                 confidence: float = 1.0, error: Optional[str] = None):
        self.success = success
        self.result = result
        self.reasoning_chain = reasoning_chain
        self.confidence = confidence
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "result": self.result,
            "reasoning_chain": [step.to_dict() for step in self.reasoning_chain],
            "confidence": self.confidence,
            "error": self.error
        }


class BaseEngine(ABC):
    DOMAIN: str = "base"
    
    def __init__(self, rules: Optional[Dict[str, Any]] = None):
        self.rules = rules or {}
        self.reasoning_chain: List[ReasoningStep] = []

    @abstractmethod
    def calculate(self, birth_date: datetime, birth_time: str, 
                  timezone: str, location: str) -> CalculationResult:
        pass

    def add_reasoning_step(self, rule_id: str, description: str,
                          input_data: Dict[str, Any], output_data: Dict[str, Any],
                          confidence: float = 1.0):
        step = ReasoningStep(rule_id, description, input_data, output_data, confidence)
        self.reasoning_chain.append(step)

    def clear_reasoning_chain(self):
        self.reasoning_chain = []

    def get_reasoning_chain(self) -> List[ReasoningStep]:
        return self.reasoning_chain
