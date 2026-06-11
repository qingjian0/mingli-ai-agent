from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routes import router
from ..config import settings
from ..core.exceptions import MingLiException
from ..persistence.database import engine
from ..persistence.models.user import Base
from ..persistence.models.computation import Base as ComputationBase
from datetime import datetime
import logging
import os

Base.metadata.create_all(bind=engine)
ComputationBase.metadata.create_all(bind=engine)

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(settings.log_file),
        logging.StreamHandler()
    ]
)

app = FastAPI(
    title=settings.app_name,
    description="企业级术数推理命理智能体API服务 - 支持全7大术数域",
    version=settings.app_version,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    duration = datetime.now() - start_time
    
    logging.info(
        f"Request: {request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Duration: {duration.total_seconds():.4f}s"
    )
    
    return response

@app.exception_handler(MingLiException)
async def mingli_exception_handler(request: Request, exc: MingLiException):
    logging.error(f"MingLiException: {exc.message} - Details: {exc.details}")
    return JSONResponse(
        status_code=exc.code,
        content={"message": exc.message, "details": exc.details}
    )

app.include_router(router, prefix=settings.api_prefix)

@app.get("/")
async def root():
    return {
        "message": "Welcome to MingLi AI Agent API",
        "version": settings.app_version,
        "environment": settings.environment,
        "domains": [
            {"id": "bazi", "name": "八字", "status": "available"},
            {"id": "ziwei", "name": "紫微斗数", "status": "available"},
            {"id": "qimen", "name": "奇门遁甲", "status": "available"},
            {"id": "liuren", "name": "大六壬", "status": "available"},
            {"id": "meihua", "name": "梅花易数", "status": "available"},
            {"id": "liuyao", "name": "六爻", "status": "available"},
            {"id": "taiyi", "name": "太乙数", "status": "available"}
        ],
        "docs": settings.docs_url
    }