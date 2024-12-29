"""
https://console.cloud.google.com/
1. GCP Console, Project Set
2. API 및 서비스 -> 사용자 인증 정보 -> OAuth 클라이언트 ID
3. (최초 설정) 동의 화면 구성
4. OAuth 클라이언트 ID 구성 및 다운로드
    - 애플리케이션 유형
    - 이름
    - 승인된 Redirection URI
5. .env 파일 생성 및 정보 입력
"""
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

app = FastAPI()

# session & secret config
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, https_only=True)

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# OAuth 설정
oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


# 1. 로그인 시작
@app.get("/auth/login")
async def login(request: Request):
    redirect_uri = "http://127.0.0.1:8000/auth/callback"  # 콜백 URI
    return await oauth.google.authorize_redirect(request, redirect_uri)


# 2. 콜백 처리
@app.get("/auth/callback")
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to fetch user info")
    return {"email": user_info["email"], "name": user_info["name"]}


# 3. 보호된 엔드포인트
@app.get("/protected")
async def protected_endpoint(request: Request):
    user = request.session.get("user")  # 세션에서 사용자 정보 가져오기
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": "Access granted", "user": user}


if __name__ == "__main__":
    uvicorn.run("oidc_oauth_google:app", host="127.0.0.1", port=8000, reload=True)
