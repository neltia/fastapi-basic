import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException

app = FastAPI()

todo_list = {
    "todo_first": "prev job execute",
    "todo_second": "current job execute"
}


# default fastapi HTTP Exception handler by starlette
# - Global: {"detail":"Not Found"}
@app.get("/todos/{todo_id}")
async def read_todo(todo_id: str):
    if todo_id not in todo_list:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo_list[todo_id]


# app run as debug
if __name__ == "__main__":
    uvicorn.run("error_handler_test:app", port=8000, reload=True)
