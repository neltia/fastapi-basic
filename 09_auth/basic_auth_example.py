import uvicorn
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter()
basic = HTTPBasic()

inner_user_name = "admin"
inner_user_pw = "admin"


# Basic auth test
@router.get("/who")
async def check_user(creds: HTTPBasicCredentials = Depends(basic)) -> dict:
    if (creds.username == inner_user_name and creds.password == inner_user_pw):
        return {"username": creds.username, "password": creds.password}
    return HTTPException(status_code=401, detail="Unauthenticated user")


if __name__ == "__main__":
    uvicorn.run("basic_auth_example:router", reload=True)
