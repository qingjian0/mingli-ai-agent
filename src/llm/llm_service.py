from typing import Optional, Dict, Any, List
from ..config import settings
from ..core.exceptions import LLMException

class LLMService:
    def __init__(self):
        self.client = None
        self._init_client()
    
    def _init_client(self):
        if not settings.openai_api_key:
            return
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=settings.openai_api_key)
        except ImportError:
            pass
    
    async def explain_result(self, domain: str, result: Dict[str, Any], 
                            user_question: Optional[str] = None) -> str:
        if not self.client:
            raise LLMException(message="LLM服务未配置，请设置OPENAI_API_KEY")
        
        system_prompt = f"""
        你是一位精通中国传统术数的专家。请用通俗易懂的语言解释{domain}计算结果。
        
        要求：
        1. 使用中文回复
        2. 解释要详细但不晦涩
        3. 避免使用过于专业的术语，必要时解释术语含义
        4. 结构清晰，可以使用分点说明
        5. 如果用户有具体问题，请针对性回答
        """
        
        user_prompt = f"""
        计算结果：{result}
        
        用户问题：{user_question or '请解释这个命盘'}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens
            )
            return response.choices[0].message.content
        
        except Exception as e:
            raise LLMException(message=f"LLM调用失败: {str(e)}")
    
    async def summarize_analysis(self, analyses: List[Dict[str, Any]]) -> str:
        if not self.client:
            raise LLMException(message="LLM服务未配置，请设置OPENAI_API_KEY")
        
        system_prompt = """
        你是一位命理分析专家。请综合多个术数分析结果，给出一个全面的总结报告。
        
        要求：
        1. 使用中文回复
        2. 综合各个术数的分析结果
        3. 指出各术数之间的一致性和差异
        4. 给出综合建议
        5. 结构清晰，使用标题和分点
        """
        
        user_prompt = f"""
        多个术数分析结果：{analyses}
        
        请给出综合总结报告。
        """
        
        try:
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens
            )
            return response.choices[0].message.content
        
        except Exception as e:
            raise LLMException(message=f"LLM调用失败: {str(e)}")