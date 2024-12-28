import uvicorn
from fastapi import FastAPI, APIRouter

app = FastAPI()

# 사용자 관련 라우터
user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/")
def get_users():
    return [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]


@user_router.post("/", status_code=201)
def create_user(name: str):
    return {"id": 3, "name": name}


# 라우터 등록
app.include_router(user_router)


# app run as debug
if __name__ == "__main__":
    uvicorn.run("api_router_default:app", port=8000, reload=True)
