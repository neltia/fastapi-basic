import uvicorn
from fastapi import FastAPI, Request, HTTPException
from common.error_handler_custom import generic_exception_handler, http_exception_handler
import time
import logging

from dotenv import load_dotenv
from app_mariadb.routes import mariadb_router


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Database CRUD API", version="1.0")
app.openapi_version = "3.0.2"

# Custom Error handler
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


# middleware: API 요청 시간 로깅
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.perf_counter()  # 요청 시작 시간
    response = await call_next(request)  # 다음 처리로 넘어감
    end_time = time.perf_counter()  # 요청 종료 시간

    process_time = end_time - start_time
    logger.info(f"Request: {request.method} {request.url} completed in {process_time:.4f} seconds")
    return response


# Include routers
app.include_router(mariadb_router, prefix="/mariadb", tags=["MariaDB"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Database CRUD API"}


# app run as debug
if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True)
