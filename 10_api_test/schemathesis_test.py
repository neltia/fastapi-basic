"""
schemathesis run --stateful=links http://localhost:8000/openapi.json
pytest --hypothesis-show-statistics
"""
import schemathesis
from hypothesis import settings

# Schemathesis로 OpenAPI 스펙 로드
url = "http://localhost:8000/openapi.json"
schema = schemathesis.from_uri(url)


# Schemathesis Test
# - Hypothesis 설정 (예: 최대 실행 시간과 예제 수 조정)
@settings(max_examples=1)  # deadline=5000
@schema.parametrize()
def test_api(case):
    case.call_and_validate()
