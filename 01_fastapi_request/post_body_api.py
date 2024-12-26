import uvicorn
from fastapi import FastAPI
from fastapi import Form, File, UploadFile
from pydantic import BaseModel
from typing import Annotated, List

app = FastAPI()

class FormData(BaseModel):
    username: str
    password: str


# form field:
# required: python-multipart
@app.post("/login/opt/")
async def login_opt(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}


# form model:
# with defined pydantic model
@app.post("/login/opt2")
async def login_opt2(data: Annotated[FormData, Form()]):
    return data


# file request form
# - bytes 형식으로 선언 시 전체 내용이 메모리에 저장돼 작은 크기 파일에 적합
@app.post("/file/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


# - UploadFile: 최대 크기 제한까지만 메모리에 저장, 이후 디스크에 저장
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


# 다중 파일 업로드
@app.post("/files/")
async def create_files(files: List[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile]):
    return {"filenames": [file.filename for file in files]}


# form & file request
@app.post("/files/request")
async def create_file_request(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }


# app run as debug
if __name__ == "__main__":
    uvicorn.run("post_body_api:app", port=8003, reload=True)
