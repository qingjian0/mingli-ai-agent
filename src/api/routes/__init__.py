from fastapi import APIRouter
from . import bazi, ziwei, analysis, qimen, liuren, meihua, liuyao, taiyi, auth, chat

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["认证"])
router.include_router(bazi.router, prefix="/bazi", tags=["八字"])
router.include_router(ziwei.router, prefix="/ziwei", tags=["紫微斗数"])
router.include_router(qimen.router, prefix="/qimen", tags=["奇门遁甲"])
router.include_router(liuren.router, prefix="/liuren", tags=["大六壬"])
router.include_router(meihua.router, prefix="/meihua", tags=["梅花易数"])
router.include_router(liuyao.router, prefix="/liuyao", tags=["六爻"])
router.include_router(taiyi.router, prefix="/taiyi", tags=["太乙数"])
router.include_router(analysis.router, prefix="/analysis", tags=["综合分析"])
router.include_router(chat.router, prefix="/chat", tags=["聊天"])