"""
Referer.
https://www.unkey.com/
https://www.unkey.com/docs/libraries/py/async
https://github.com/unkeyed/unkey
https://blog.naver.com/dsz08082/223451099783
"""
import uvicorn
from fastapi import FastAPI, Header, Depends, status, HTTPException
from fastapi import Security
from fastapi.security import APIKeyHeader

from pydantic import BaseModel
from typing import Optional, Dict, Union
import unkey
from unkey.undefined import UNDEFINED
import os
from dotenv import load_dotenv

# main app init
app = FastAPI()
authorize_key = APIKeyHeader(name="Authorization", auto_error=True)


# model: api key input model
class api_key_create(BaseModel):
    name: str = ""
    owner_id: str = "test-user"
    prefix: str = ""

    remaining: Optional[int] = None
    meta: Optional[Dict] = None
    expires: Union[int, None] = None


# depends: header key check
async def authorize_key_required(authorize_key=Security(APIKeyHeader(name="Authorization"))):
    if authorize_key is None or authorize_key == "":
        raise HTTPException(status_code=401, detail="not found key")
    return authorize_key


# logic: api key validate
async def is_key_verify(request_key: str):
    unkey_api_id = os.environ["UNKEY_API_ID"]

    client = unkey.Client()
    await client.start()
    result = await client.keys.verify_key(key=request_key, api_id=unkey_api_id)

    if result.is_ok:
        result_data = result._value.to_dict()
        return result_data["valid"], result_data["code"]
    else:
        return False, result.unwrap_err()


# logic: api key create
async def create_api_key(authorize_key: str, api_key_create: api_key_create):
    unkey_root_key = os.environ["UNKEY_ROOT_KEY"]
    unkey_api_id = os.environ["UNKEY_API_ID"]

    if authorize_key != unkey_root_key:
        return False, ""

    key_request = api_key_create.model_dump()
    # print(key_request)
    owner_id = key_request["owner_id"]
    prefix = key_request["prefix"]
    meta = key_request["meta"]
    expires = key_request["expires"]

    if len(key_request["meta"].keys()) > 0:
        meta = UNDEFINED
    if expires == 0:
        expires = UNDEFINED

    client = unkey.Client(api_key=unkey_root_key)
    await client.start()
    result = await client.keys.create_key(
        api_id=unkey_api_id, owner_id=owner_id, prefix=prefix,
        meta=meta, expires=expires
    )

    if result.is_ok:
        result_data = result._value.to_dict()
        return True, result_data
    else:
        return False, result.unwrap_err()


# controller. 키 인증 여부 확인
@app.get("/verify")
async def protected_route(x_api_key: str = Header(None)):
    status_code = status.HTTP_200_OK

    if x_api_key is None or x_api_key.strip() == "":
        status_code = status.HTTP_400_BAD_REQUEST
        error_msg = "not found key"
        return {"result_code": status_code, "result_msg": error_msg}

    res_code, res_msg = await is_key_verify(request_key=x_api_key)
    if not res_code:
        status_code = status.HTTP_401_UNAUTHORIZED
        msg = "unvalid key"
        return {"result_code": status_code, "result_msg": msg}

    msg = "valid"
    return {"result_code": status_code, "result_msg": msg}


# 새 API 키 생성
@app.post("/token", status_code=201, dependencies=[Depends(authorize_key_required)])
async def token_generate(api_key_create: api_key_create, authorize_key: str = Depends(authorize_key_required)) -> dict:
    status_code = status.HTTP_201_CREATED

    res_code, res_msg = await create_api_key(authorize_key, api_key_create)
    if not res_code:
        status_code = status.HTTP_401_UNAUTHORIZED
        return {"result_code": status_code, "result_msg": res_msg}

    return {"result_code": status_code, "result_msg": res_msg}


# app run as debug
if __name__ == "__main__":
    load_dotenv()
    uvicorn.run("third_auth_unkey:app", port=8000, reload=True)
