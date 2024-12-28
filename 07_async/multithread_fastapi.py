from fastapi import FastAPI, Depends
from concurrent.futures import ThreadPoolExecutor
import asyncio
import threading
import time
from logger.logger_decorator import log_request_time
from logger.logger_depends import depend_log_request

app = FastAPI()

# ThreadPoolExecutor 생성
executor = ThreadPoolExecutor(max_workers=5)  # 스레드풀에서 최대 5개 작업 실행


# ------------------------------
# 동기 함수: 멀티스레드용
# ------------------------------
def threaded_task(name: str):
    """멀티스레드에서 실행할 동기 작업"""
    print(f"[{threading.current_thread().name}] Start task: {name}")
    time.sleep(3)  # 동기 대기
    print(f"[{threading.current_thread().name}] End task: {name}")
    return {"message": f"Task {name} completed"}


# ------------------------------
# 멀티스레드 직접 활용
# ------------------------------
@app.get("/multithread")
@log_request_time
def multithread_endpoint():
    """멀티스레드에서 작업 실행"""
    threads = []
    for i in range(3):
        thread = threading.Thread(target=threaded_task, args=(f"Thread-{i+1}",))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  # 모든 스레드가 끝날 때까지 대기

    return {"message": "All threads completed"}


# ------------------------------
# 스레드풀 활용
# ------------------------------
@app.get("/threadpool", dependencies=[Depends(depend_log_request)])
async def threadpool_endpoint():
    """스레드풀에서 동기 작업 실행"""
    loop = asyncio.get_event_loop()
    results = await asyncio.gather(
        loop.run_in_executor(executor, threaded_task, "Pool-1"),
        loop.run_in_executor(executor, threaded_task, "Pool-2"),
        loop.run_in_executor(executor, threaded_task, "Pool-3"),
    )
    return {"results": results}


# ------------------------------
# 비동기 함수와 멀티스레드 혼합
# ------------------------------
async def async_task(name: str):
    """비동기 작업"""
    print(f"[{threading.current_thread().name}] Async task: {name}")
    await asyncio.sleep(3)  # 비동기 대기
    print(f"[{threading.current_thread().name}] Async task completed: {name}")
    return {"message": f"Async task {name} completed"}


@app.get("/mixed")
@log_request_time
async def mixed_endpoint():
    """비동기 작업과 스레드 작업 혼합 실행"""
    loop = asyncio.get_event_loop()
    # 멀티스레드에서 실행
    thread_results = await asyncio.gather(
        loop.run_in_executor(executor, threaded_task, "Mixed-Thread-1"),
        loop.run_in_executor(executor, threaded_task, "Mixed-Thread-2"),
    )

    # 비동기 작업 실행
    async_results = await asyncio.gather(
        async_task("Mixed-Async-1"),
        async_task("Mixed-Async-2"),
    )

    return {"thread_results": thread_results, "async_results": async_results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("multithread_fastapi:app", host="127.0.0.1", port=8000, reload=True)
