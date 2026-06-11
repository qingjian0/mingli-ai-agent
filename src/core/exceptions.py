from typing import Optional, Dict, Any
from fastapi import HTTPException, status

class MingLiException(Exception):
    code: int = 500
    message: str = "服务器内部错误"
    details: Optional[Dict[str, Any]] = None
    
    def __init__(self, message: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        if message:
            self.message = message
        if details:
            self.details = details
        super().__init__(self.message)
    
    def to_http_exception(self) -> HTTPException:
        return HTTPException(
            status_code=self.code,
            detail={"message": self.message, "details": self.details}
        )

class ValidationException(MingLiException):
    code = 400
    message = "请求参数验证失败"

class AuthenticationException(MingLiException):
    code = 401
    message = "未授权访问"

class AuthorizationException(MingLiException):
    code = 403
    message = "权限不足"

class NotFoundException(MingLiException):
    code = 404
    message = "资源不存在"

class RateLimitException(MingLiException):
    code = 429
    message = "请求过于频繁"

class CalculationException(MingLiException):
    code = 400
    message = "计算失败"

class LLMException(MingLiException):
    code = 503
    message = "LLM服务暂时不可用"