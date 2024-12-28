"""
FastAPI Dendency Injection (의존성 주입)

의존성: 어떤 시점에 필요한 특정 정보
다음 작업을 로직 내부가 아닌 FastAPI 요청 단에서 처리
- HTTP 요청에서 입력 값 저장
- 입력 값 유효성 검사
- 인증/인가 권한 확인
- 데이터 소스(DB)에서 데이터 조회
- 로그, 지표(Metric) 정보 추적

단점: 테스트를 위한 함수 변경 불가, 로직 상 중복 호출 문제, Swagger 등록 로직 추가 필요
"""
import uvicorn
from fastapi import FastAPI
from fastapi import Depends, Query, HTTPException
from fastapi import APIRouter

app = FastAPI()
# app = FastAPI(dependencies=[Depends()]) # global Depends scope
# router = APIRouter(dependencies=[Depends()]) # router based Depends scope


# func. user info input
async def user_dep(name: str = Query(..., description="User name"),
                   gender: str = Query(..., description="User gender")):
    return {"name": name, "valid": True}


# func. user valid check
async def user_check_dep(name: str = Query(...), gender: str = Query(...)):
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")


# Depends. common param validation
@app.get("/user")
async def get_user(user: dict = Depends(user_dep)) -> dict:
    return user


@app.get("/user/check")
async def check_user(user: dict = Depends(user_check_dep)) -> dict:
    return user


# app run as debug
if __name__ == "__main__":
    uvicorn.run("dependency_injection:app", port=8000, reload=True)
