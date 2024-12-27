from pydantic import BaseModel, Field
from typing import Dict, Optional, Any

from datetime import datetime
import json
from urllib.parse import unquote


class RequestUser(BaseModel):
    api_key: str


class APIRequest(BaseModel):
    api_code: int
    request_date: str
    request_url: str
    params: Optional[Dict[str, Any]] = Field(default_factory=dict)
    user: RequestUser


class APIResponse(BaseModel):
    api_http_status: int
    api_result_code: Optional[int] = None
    diff_status: str
    diff_msg: Optional[str]
    elapsed_time: float


class APITestResult(BaseModel):
    request: APIRequest
    response: APIResponse


# parse http request params
def get_request_params(api_response):
    request = api_response.request
    method = request.method
    content_type = request.headers.get('Content-Type', "")

    if method == "GET":
        request_url = request.url
        if "?" not in request_url:
            return None

        query_string = request_url.split('?', 1)[1]
        return dict(param.split('=') for param in query_string.split('&')) if query_string else {}

    if method == "POST":
        body = getattr(request, 'body', "")
        if content_type == "application/json":
            return json.loads(body) if body else {}
        elif content_type == "application/x-www-form-urlencoded":
            return dict(pair.split('=') for pair in body.split('&')) if body else {}

    return None


# get result code from api request response
def get_result_code(api_response):
    try:
        api_response_json = api_response.json()
    except Exception:
        return None

    if "result_code" in api_response_json:
        result_code = api_response_json["result_code"]

    return result_code


def build_api_request(api_code, api_response):
    now_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request_date = api_response.request.headers.get("request_time", now_date)
    request_url = api_response.request.url
    params = get_request_params(api_response)
    api_key = "dummey_key"

    api_request = APIRequest(
        api_code=api_code,
        request_date=request_date,
        request_url=unquote(request_url),
        params=params,
        user=RequestUser(api_key=api_key)
    )
    return api_request


def build_diff_response(api_response, diff_status, diff_msg):
    api_http_status = api_response.status_code
    api_result_code = get_result_code(api_response)
    elapsed_time = api_response.elapsed.total_seconds()

    diff_response = APIResponse(
        api_http_status=api_http_status,
        api_result_code=api_result_code,
        diff_status=diff_status,
        diff_msg=diff_msg,
        elapsed_time=elapsed_time
    )
    return diff_response


def build_result_data(api_code, api_response, diff_status, diff_msg):
    api_request = build_api_request(api_code, api_response)
    diff_response = build_diff_response(api_response, diff_status, diff_msg)
    result = APITestResult(request=api_request, response=diff_response)
    return result
