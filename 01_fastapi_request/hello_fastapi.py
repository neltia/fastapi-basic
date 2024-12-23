from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"msg": "Hello World"}


# app run as debug
if __name__ == "__main__":
    uvicorn.run("hello_fastapi:app", port=8000, reload=True)
