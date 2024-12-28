import uvicorn
from fastapi import FastAPI, HTTPException
from common.error_handler_custom import generic_exception_handler, http_exception_handler

from dotenv import load_dotenv
from app_mariadb.routes import mariadb_router


load_dotenv()

app = FastAPI(title="Database CRUD API", version="1.0")

# Custom Error handler
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include routers
app.include_router(mariadb_router, prefix="/mariadb", tags=["MariaDB"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Database CRUD API"}


# app run as debug
if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True)
