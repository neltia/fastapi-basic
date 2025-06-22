from fastapi import FastAPI
from app.controllers.user_controller import router as user_router
from app.core.config import settings

app = FastAPI()

# Async mode 설정을 기반으로 라우터 추가
if settings.async_mode:
    print("[Main] Using ASYNC mode")
else:
    print("[Main] Using SYNC mode")

app.include_router(user_router, prefix="/api/v1")
