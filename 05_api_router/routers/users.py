from fastapi import APIRouter

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/")
def get_users():
    return [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]


@user_router.post("/", status_code=201)
def create_user(name: str):
    return {"id": 3, "name": name}
