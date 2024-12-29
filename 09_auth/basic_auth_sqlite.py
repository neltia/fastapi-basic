import uvicorn
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request, Response
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from sqlalchemy.orm import Session
from sqlite_user.db import Base, engine, get_db
from sqlite_user.schemas import UserCreate, PasswordUpdate, UserResponse
from sqlite_user.service import UserService

router = APIRouter()

Base.metadata.create_all(bind=engine)


# login: 사용자 이름과 비밀번호를 검증하여 접근 허용 (cookie)
@router.post("/login/cookie", tags=["Login"])
def login_with_cookie(
    response: Response,
    credentials: HTTPBasicCredentials = Depends(HTTPBasic()),
    db: Session = Depends(get_db)
):
    login_data = UserService.authenticate_user(db, credentials.username, credentials.password)

    # 쿠키에 로그인 정보 저장 (보안 향상을 위해 HttpOnly 설정)
    response.set_cookie(key="logged_in_user", value=login_data["username"], httponly=True)
    return login_data


# login: 사용자 이름과 비밀번호를 검증하여 접근 허용 (session)
@router.post("/login", tags=["Login"])
def login_with_session(
    request: Request,
    credentials: HTTPBasicCredentials = Depends(HTTPBasic()),
    db: Session = Depends(get_db)
):
    login_data = UserService.authenticate_user(db, credentials.username, credentials.password)

    # 세션에 로그인 정보 저장
    request.session["username"] = login_data["username"]
    return login_data


# 현재 로그인된 사용자 정보 반환
@router.post("/me", tags=["Login"])
def get_logged_in_user(request: Request):
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=401, detail="User not logged in")
    return {"username": username}


# 세션 정보 제거
@router.post("/logout", tags=["Login"])
def logout(request: Request):
    request.session.clear()
    return {"message": "Logout successful"}


# registered user list
@router.get("/users", response_model=list[UserResponse], tags=["User"])
def list_users(db: Session = Depends(get_db)):
    return UserService.list_users(db)


# creat user
@router.post("/users", response_model=UserResponse, status_code=201, tags=["User"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db, user)


# get user data
@router.get("/users/{username}", response_model=UserResponse, tags=["User"])
def get_user(username: str, db: Session = Depends(get_db)):
    return UserService.get_user(db, username)


# update user data
@router.put("/users/{username}", response_model=UserResponse, tags=["User"])
def update_user(username: str, password_update: PasswordUpdate, db: Session = Depends(get_db)):
    return UserService.update_user(db, username, password_update.current_password, password_update.new_password)


# delete user data
@router.delete("/users/{username}", tags=["User"])
def delete_user(username: str, db: Session = Depends(get_db)):
    return UserService.delete_user(db, username)


if __name__ == "__main__":
    uvicorn.run("basic_auth_sqlite:router", reload=True)
