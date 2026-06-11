from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    app_name: str = "MingLi-AI-Agent"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = False
    
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    
    database_url: str = "sqlite:///./mingli.db"
    database_test_url: str = "sqlite:///./test.db"
    
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_echo: bool = False
    
    redis_url: str = "redis://localhost:6379/0"
    redis_timeout: int = 5
    redis_max_connections: int = 10
    
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.1
    llm_max_tokens: int = 4096
    
    secret_key: str = "mingli-ai-agent-secret-key-change-in-production-2024"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    
    rate_limit_max_requests: int = 1000
    rate_limit_window_seconds: int = 3600

settings = Settings()