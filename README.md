# FastAPI-Basic
## Intro
fastapi 기능을 점진적으로 학습할 수 있도록 구성 <br>
This repository is organized into various steps to progressively learn FastAPI features

### Directory Structure

```plaintext
fastapi-basic/
│
├── 01_fastapi_request/
├── 02_fastapi_response/
├── 03_pydantic_validation/
├── 04_template_response/
│   ├── static/
│   ├── templates_bootstrap/
│   ├── templates_jinja2/
│   └── templates_tailwind/
├── 05_api_router/
│   └── routers/
├── 06_fastapi_depends/
├── 07_async/
│   └── logger/
├── 08_db_app/
│   ├── app_mariadb/
│   └── common/
├── 09_auth/
│   └── sqlite_user/
└── 10_api_test/
```

### Getting Started
- python 3.10+
- FastAPI
- Uvicorn (ASGI server)
- Other dependencies as listed in `requirements.txt`

#### Installation
- Clone the repository:
   ```bash
   git clone https://github.com/neltia/fastapi-basic.git
   cd fastapi-basic
   ```

- virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
