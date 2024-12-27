"""
FastAPI Response Class
- JSONResponse: JSON 타입 Content 전송. Python object -> json format 자동 변환
- HTMLResponse: HTML Content 전송
- RedirectResponse: 요청 처리 후 다른 URL로 Client를 다른 URL로 Redirect
- PlainTextResponse: 일반 text Content 전송
- FileResponse: 파일 download 처리에 사용
- StreamingResponse: 대용량 파일의 Streaming이나 chat message 등에 사용
"""
import uvicorn
from datetime import datetime
from typing import Union

from fastapi import FastAPI
from fastapi import Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, ORJSONResponse, PlainTextResponse
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Union[str, None] = None


# regacy response
# - content에 응답 데이터
# - media_type에 resposne Content-Type 값 직접 명시
@app.get("/legacy/xml")
async def get_legacy_xml():
    data = """\
    <?xml version="1.0"?>
    <shampoo>
        <Header>
            Apply shampoo here.
        </Header>
        <Body>
            You'll have to use soap here.
        </Body>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")


# json response example
# JSONResponse: Response' sub class
# content-type 응답 헤더 값은 JSONResponse가 자동 처리
#  pydantic model dump -> JSONResponss에 넣지 않으면,
#  datetime 등 호환되지 않는 값 누락/오류 발생
@app.put("/item/{item_id}")
async def item_res_json(item_id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    return JSONResponse(content=json_compatible_item_data)


# orjson response example
# orjson lib based dict data return
# * required: pip install orjson
# - response_class: Specifies response data format and MIME type
# - response_model: Validates response data format and structure, and adds schema to Swagger docs
@app.get("/item/orjson", response_class=ORJSONResponse)
async def item_res_orjson():
    item = Item(
        title="fastapi study",
        timestamp=datetime.now(),
        description="fastapi respons class study"
    )
    return ORJSONResponse(content=item.model_dump_json())


@app.get("/item/text", response_class=PlainTextResponse)
async def item_res_text():
    item = Item(
        title="fastapi study",
        timestamp=datetime.now(),
        description="fastapi respons class study"
    )
    return PlainTextResponse(content=item.model_dump_json())


# html response example
@app.get("/index/", response_class=HTMLResponse)
async def get_index():
    html_example = """\
        <html><body><h1>Hello, World!</h1></body></html>
    """
    return html_example


# redirect response example
@app.get("/redirect")
async def get_redirect():
    return RedirectResponse(url="/index/")


# file response
# - 파일을 다운로드하거나 표시
# - Content-Disposition 헤더를 통해 다운로드 처리
# - media-type를 지정해 응답 미디어 타입 지정 가능
@app.get("/file/download")
async def get_file():
    file_path = "json_response.py"
    return FileResponse(file_path, media_type="text/plain", filename="download.txt")


# streaming response
# - 스트리밍 방식 데이터 응답, 대량 데이터를 청크 단위로 로드
# - 실시간 데이터 스트리밍, 대규모 파일 전송, 비디오/오디오 스트리밍 시 사용
async def fake_video_streamer():
    for i in range(10):
        yield f"Frame {i}\n"


@app.get("/stream", response_class=StreamingResponse)
async def stream():
    return StreamingResponse(fake_video_streamer(), media_type="text/plain")


# app run as debug
if __name__ == "__main__":
    uvicorn.run("response_class_api:app", port=8000, reload=True)
