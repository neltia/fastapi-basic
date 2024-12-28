from fastapi import Request
from datetime import datetime
import time


# ------------------------------
# 요청 로깅 의존성
# ------------------------------
async def depend_log_request(request: Request):
    """
    요청-응답 시간과 실행 시간을 로깅하는 의존성 함수.
    """
    # 요청 시작 시간 기록
    start_time = time.time()
    start_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Request received at: {start_dt}")

    # 요청 객체 반환 (엔드포인트에서 필요할 경우 사용 가능)
    yield request

    # 응답 종료 시간 기록
    end_time = time.time()
    end_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_time = end_time - start_time
    print(f"Response sent at: {end_dt}")
    print(f"Total execution time: {total_time:.2f} seconds")
