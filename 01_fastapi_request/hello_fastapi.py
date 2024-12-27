from fastapi import FastAPI
from fastapi import Request
import uvicorn

app = FastAPI()


# default route
@app.get("/")
async def root():
    return {"msg": "Hello World"}


# fastapi Request data info
@app.get("/info")
async def get_info(request: Request):
    client_host = request.client.host
    headers = request.headers
    query_params = request.query_params

    data = {
        "request_method": request.method,
        "request_url": str(request.url),
        "client_host": client_host,
        "headers": headers,
        "cookies": request.cookies,
        "query_params": query_params
    }
    return data


# app run as debug
if __name__ == "__main__":
    uvicorn.run("hello_fastapi:app", port=8000, reload=True)
