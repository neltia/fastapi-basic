"""
CustomRoute 클래스 구현 시
- 요청 로깅/응답 검증 등 공통 적용 동작 중앙 제어 -> 유사 미들웨어 역할
- 특정 router에만 적용 가능, 유연한 확장성 기대
- 관리 복잡성 증가와 미들웨어가 적합한 경우 선별 필요 등 단점 존재
"""
import uvicorn
from fastapi import FastAPI, APIRouter, Request
from fastapi.routing import APIRoute


class CustomRoute(APIRoute):
    def get_route_handler(self):
        original_handler = super().get_route_handler()

        async def custom_handler(request: Request):
            print(f"Custom logging: {request.method} {request.url}")
            response = await original_handler(request)
            print(f"Response status: {response.status_code}")
            return response

        return custom_handler


# 사용자 라우터
user_router = APIRouter(route_class=CustomRoute, prefix="/users", tags=["users"])


@user_router.get("/")
async def get_users():
    return [{"id": 1, "name": "John"}]


app = FastAPI()
app.include_router(user_router)


# app run as debug
if __name__ == "__main__":
    uvicorn.run("api_router_custom:app", port=8000, reload=True)
