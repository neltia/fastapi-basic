from functools import wraps
from datetime import datetime
import time
import inspect


# ------------------------------
# 실행 시간 측정 데코레이터
# ------------------------------
def log_request_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # 요청 시작 시간 기록
        start_time = time.time()
        start_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Request received at: {start_dt}")

        # 동기/비동기 함수 처리 분기
        if inspect.iscoroutinefunction(func):
            response = await func(*args, **kwargs)  # 비동기 함수
        else:
            response = func(*args, **kwargs)  # 동기 함수

        # 응답 종료 시간 기록
        end_time = time.time()
        end_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_time = end_time - start_time
        print(f"Response sent at: {end_dt}")
        print(f"Total execution time: {total_time:.2f} seconds")

        return response
    return wrapper
