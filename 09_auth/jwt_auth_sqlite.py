"""
JWT Request Flow
1. user join     -> POST /users
2. user login    -> POST /token : access_token & refresh token
3. user check    -> GET /users/me : access_token validation
4. token reissue -> GET /refresh : refresh_token validation & access_token reissue
5. logout
"""
import uvicorn
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security.api_key import APIKeyHeader

from sqlalchemy.orm import Session
from sqlite_user.db import Base, engine, get_db
from sqlite_user.service import UserService
from sqlite_user.jwt_security import create_access_token, create_refresh_token, decode_token

router = APIRouter(tags=["JWT Authentication"])

# 데이터베이스 초기화
Base.metadata.create_all(bind=engine)

# OAuth2PasswordBearer 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)  # for jwt token


# JWT 토큰 검증 후 사용자 정보 반환
def get_current_user(api_key: str = Security(api_key_header)):
    if not api_key or not api_key.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing Authorization header"
        )

    token = api_key[len("Bearer "):]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return {"username": username}


# 토큰 검증 절차를 거쳐 확인된 사용자 정보 반환
@router.get("/users/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user


# access_token과 refresh_token 발급
@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = UserService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # 토큰 발급
    access_token = create_access_token(data={"sub": user["username"]})
    refresh_token = create_refresh_token(data={"sub": user["username"]})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


# 리프레시 토큰을 통해 새로운 access_token 발급
@router.post("/refresh")
def refresh_token(
    refresh_token: str, db: Session = Depends(get_db)
):
    payload = decode_token(refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    username: str = payload.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # 새 access_token 발급
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run("jwt_auth_sqlite:router", reload=True, port=8001)
