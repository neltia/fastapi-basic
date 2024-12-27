import uvicorn
from fastapi import FastAPI
from fastapi import Cookie, Header
from typing import Annotated, Union, List

app = FastAPI()


# Query/Path 방식으로 Cookie, Header 호출 가능
@app.get("/cookie/")
async def get_cookie(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}


# opt) convert_underscores:
# - 표준 헤더를 사용하기 위해 언더스코어(-) -> 하이픈(-)으로 자동 변환
@app.get("/header/")
async def get_header(user_agent: Union[str, None] = Header(default=None, convert_underscores=True)):
    return {"User-Agent": user_agent}


# opt) 다중 값을 갖는 동일한 헤더 수신
@app.get("/header/list")
async def get_header_list(x_token: Union[List[str], None] = Header(default=None)):
    return {"X-Token values": x_token}


# app run as debug
if __name__ == "__main__":
    uvicorn.run("get_header_api:app", port=8004, reload=True)
