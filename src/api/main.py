
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import bazi, ziwei, analysis
from .. import __version__

app = FastAPI(
    title="MingLi AI Agent API",
    description="企业级术数推理命理智能体API服务",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bazi.router, prefix="/api/v1/bazi", tags=["八字"])
app.include_router(ziwei.router, prefix="/api/v1/ziwei", tags=["紫微斗数"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["综合分析"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to MingLi AI Agent API",
        "version": __version__,
        "docs": "/docs"
    }
