from fastapi import FastAPI
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

app = FastAPI()

# ThreadPoolExecutor 생성
executor = ThreadPoolExecutor(max_workers=5)  # 최대 5개의 스레드 사용


# ------------------------------
# 동기(Sync) 작업
# ------------------------------
def sync_task():
    """동기 함수: CPU-집약적 작업 또는 오래 걸리는 동기 작업"""
    time.sleep(3)  # 동기적 대기
    return {"message": "Sync task completed"}


@app.get("/sync")
def sync_endpoint():
    """Sync Endpoint"""
    result = sync_task()  # 동기 함수 호출
    return result


# ------------------------------
# 비동기(Async) 작업
# ------------------------------
async def async_task():
    """비동기 함수: I/O-집약적 작업"""
    # await asyncio.sleep(3)  # 비동기적 대기
    return {"message": "Async task completed"}


@app.get("/async")
async def async_endpoint():
    """Async Endpoint"""
    result = await async_task()  # 비동기 함수 호출
    return result


# ------------------------------
# 스레드풀을 활용한 동기 함수 호출
# ------------------------------
def cpu_bound_task():
    """CPU-집약적 작업"""
    total = sum(range(10**7))  # CPU 집중 작업
    return {"result": total}


@app.get("/threadpool")
async def threadpool_endpoint():
    """스레드풀을 사용한 동기 작업 처리"""
    loop = asyncio.get_event_loop()
    # 스레드풀에서 실행
    result = await loop.run_in_executor(executor, cpu_bound_task)
    return result


# ------------------------------
# 혼합 사용 사례
# ------------------------------
async def async_with_threadpool():
    """비동기 작업 중 스레드풀을 활용"""
    loop = asyncio.get_event_loop()
    sync_result = await loop.run_in_executor(executor, cpu_bound_task)
    async_result = await async_task()
    return {"sync_result": sync_result, "async_result": async_result}


@app.get("/mixed")
async def mixed_endpoint():
    """Sync + Async 혼합 작업"""
    result = await async_with_threadpool()
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("async_fastapi:app", host="127.0.0.1", port=8000, reload=True)
