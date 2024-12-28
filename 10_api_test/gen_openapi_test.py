"""
swagger openapi json 기반 pytest 코드 틀 구성
"""
import requests
import orjson
import os
import sys


# Fetches the OpenAPI spec from the given API URL and saves it as a JSON file using orjson.
def save_openapi_spec(api_url: str, output_file: str):
    try:
        response = requests.get(api_url)
        response.raise_for_status()

        # Parse JSON response using orjson
        spec_data = response.json()

        # Save to file with orjson
        with open(output_file, "wb") as f:
            f.write(orjson.dumps(spec_data, option=orjson.OPT_INDENT_2))

        print(f"OpenAPI spec saved to {output_file}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching OpenAPI spec: {e}")
    except orjson.JSONEncodeError as e:
        print(f"Error encoding JSON with orjson: {e}")


def load_openapi_spec(file_path: str):
    # OpenAPI JSON 파일 로드
    with open(file_path, "rb") as f:
        spec_data = orjson.loads(f.read())
    return spec_data


def generate_test_files(openapi_spec, base_test_dir="tests"):
    base_url = "http://test"  # TestClient에서 사용되는 base URL
    os.makedirs(base_test_dir, exist_ok=True)

    test_file_paths = {}

    for path, methods in openapi_spec["paths"].items():
        for method, details in methods.items():
            # Grouping by tags or similar logic
            tag = details.get("tags", ["default"])[0]
            test_dir = os.path.join(base_test_dir, tag)
            os.makedirs(test_dir, exist_ok=True)

            # Single file per tag
            test_file_path = os.path.join(test_dir, "test_endpoints.py")
            if test_file_path not in test_file_paths:
                test_file_paths[test_file_path] = []

            # Append test case to the list for this file
            test_code = f"""

@pytest.mark.asyncio
async def test_{details['operationId']}():
    async with AsyncClient(app=app, base_url="{base_url}") as ac:
        response = await ac.{method.lower()}("{path}")
        assert response.status_code == 200
"""
            test_file_paths[test_file_path].append(test_code)

    # Write all test cases to their respective files
    for test_file_path, test_cases in test_file_paths.items():
        with open(test_file_path, "w") as test_file:
            # Write imports only once per file
            test_file.write("""
import pytest
from httpx import AsyncClient
from get_app import get_app

app = get_app()""".strip())
            test_file.write("\n")
            test_file.writelines(test_cases)


def main():
    api_url = "http://localhost:8000/openapi.json"
    out_path = "openapi.json"

    # openapi.json write
    if not os.path.exists(out_path):
        save_openapi_spec(api_url, out_path)

    # openapi.json read
    if not os.path.exists(out_path):
        sys.exit()
    openapi_spec = load_openapi_spec(out_path)

    # 테스트 코드 생성
    generate_test_files(openapi_spec)
    print("Test files generated in 'tests' directory.")


if __name__ == "__main__":
    os.makedirs("tests", exist_ok=True)
    main()
