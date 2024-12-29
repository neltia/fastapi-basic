from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from basic_auth_example import router as basic_router
from basic_auth_sqlite import router as sqlite_router
from jwt_auth_sqlite import router as jwt_router

# FastAPI 앱 초기화
app = FastAPI(title="Authentication API", version="1.0.0")

# Secret key for session
SECRET_KEY = "your_secret_key"
# 세션 미들웨어 추가
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# APIRouter 통합
app.include_router(basic_router, prefix="/basic", tags=["Basic Authentication"])
app.include_router(sqlite_router, prefix="/sqlite")
app.include_router(jwt_router, prefix="/jwt", tags=["JWT Authentication"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("auth_app:app", host="127.0.0.1", port=8000, reload=True)
