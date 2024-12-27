import uvicorn
from datetime import datetime

from fastapi import FastAPI
from fastapi import status
from fastapi.responses import JSONResponse
from http import HTTPStatus
from pydantic import BaseModel


app = FastAPI()


class Todo(BaseModel):
    task: str
    timestamp: datetime = datetime.now()


# creat todo
# - defualt status: 200 -> static status: 201
@app.post("/todo/opt", status_code=201)
async def create_todo_value(todo: Todo):
    return {"result_code": 201, "created_at": todo.timestamp}


# - 직접 http status code 값을 입력하거나 fastapi에서 제공하는 enum 값 활용
# - enum (str) -> value (int) 값은 제공하나, result_msg 값은 비제공
@app.post("/todo/opt2", status_code=status.HTTP_201_CREATED)
async def create_todo_status(todo: Todo):
    data = {
        "result_code": status.HTTP_201_CREATED,
        "result_msg": "Created",
        "created_at": todo.timestamp
    }
    return data


# - 파이썬 표준 라이브러리 http.HTTPStatus 사용 메시지 매핑
# - fastapi 기본 응답은 JSONResponse cotent 데이터로 래핑되며, 여기 status_code 명시 가능
@app.post("/todo/opt3")
async def create_todo_enum(todo: Todo):
    data = {
        "result_code": status.HTTP_201_CREATED,
        "result_msg": HTTPStatus(status.HTTP_201_CREATED).phrase,
        "created_at": todo.timestamp
    }
    return JSONResponse(content=data, status_code=status.HTTP_201_CREATED)


# app run as debug
if __name__ == "__main__":
    uvicorn.run("enum_response_status:app", port=8000, reload=True)
