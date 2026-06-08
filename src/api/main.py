
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import bazi, ziwei, analysis, qimen, liuren, meihua, liuyao, taiyi
from .. import __version__

app = FastAPI(
    title="MingLi AI Agent API",
    description="企业级术数推理命理智能体API服务 - 支持全7大术数域",
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
app.include_router(qimen.router, prefix="/api/v1/qimen", tags=["奇门遁甲"])
app.include_router(liuren.router, prefix="/api/v1/liuren", tags=["大六壬"])
app.include_router(meihua.router, prefix="/api/v1/meihua", tags=["梅花易数"])
app.include_router(liuyao.router, prefix="/api/v1/liuyao", tags=["六爻"])
app.include_router(taiyi.router, prefix="/api/v1/taiyi", tags=["太乙数"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["综合分析"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to MingLi AI Agent API",
        "version": __version__,
        "domains": [
            {"id": "bazi", "name": "八字", "status": "available"},
            {"id": "ziwei", "name": "紫微斗数", "status": "available"},
            {"id": "qimen", "name": "奇门遁甲", "status": "available"},
            {"id": "liuren", "name": "大六壬", "status": "available"},
            {"id": "meihua", "name": "梅花易数", "status": "available"},
            {"id": "liuyao", "name": "六爻", "status": "available"},
            {"id": "taiyi", "name": "太乙数", "status": "available"}
        ],
        "docs": "/docs"
    }
