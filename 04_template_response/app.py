import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime

app = FastAPI()

# static file
app.mount("/static", StaticFiles(directory="static"), name="static")

# 각 템플릿 경로 설정
templates = {
    "jinja2": Jinja2Templates(directory="templates_jinja2"),
    "bootstrap": Jinja2Templates(directory="templates_bootstrap"),
    "tailwind": Jinja2Templates(directory="templates_tailwind"),
}


# 공통 데이터 생성 함수
def get_template_data(request: Request, title: str, menu: list) -> dict:
    return {
        "request": request,
        "title": title,
        "menu": menu,
        "client_ip": request.client.host,
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


@app.get("/")
async def jinja2_template(request: Request):
    data = get_template_data(request, "Jinja2 Example", ["Home", "About", "Contact"])
    return templates["jinja2"].TemplateResponse("index.html", data)


@app.get("/bootstrap")
async def bootstrap_template(request: Request):
    data = get_template_data(request, "Bootstrap Example", ["Home", "Features", "Pricing"])
    return templates["bootstrap"].TemplateResponse("index.html", data)


@app.get("/tailwind")
async def tailwind_template(request: Request):
    data = get_template_data(request, "Tailwind Example", ["Dashboard", "Profile", "Settings"])
    return templates["tailwind"].TemplateResponse("index.html", data)


# app run as debug
if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True)
