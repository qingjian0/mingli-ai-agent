from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Float
from sqlalchemy.sql import func
from ..database import Base

class ComputationRequest(Base):
    __tablename__ = "computation_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    domain = Column(String(20), nullable=False)
    status = Column(String(20), default="pending")
    input_data = Column(JSON, nullable=False)
    result_data = Column(JSON)
    confidence = Column(Float)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    def __repr__(self):
        return f"<ComputationRequest(id={self.id}, domain={self.domain}, user_id={self.user_id})>"

class ComputationStep(Base):
    __tablename__ = "computation_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, nullable=False)
    step_order = Column(Integer, nullable=False)
    rule_id = Column(String(50))
    description = Column(Text)
    input_data = Column(JSON)
    output_data = Column(JSON)
    confidence = Column(Float)
    status = Column(String(20), default="completed")
    
    def __repr__(self):
        return f"<ComputationStep(request_id={self.request_id}, step_order={self.step_order})>"

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    action_type = Column(String(50), nullable=False)
    entity_type = Column(String(50))
    entity_id = Column(Integer)
    details = Column(JSON)
    ip_address = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<AuditLog(user_id={self.user_id}, action_type={self.action_type})>"