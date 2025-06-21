import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Tuple, Any, Dict
from sqlalchemy import text

from app.core.config import settings


# Database Connection Testing
def test_sync_database_connection() -> Tuple[bool, Any]:
    """Test synchronous database connection"""
    try:
        from app.db.base import SessionLocal

        db = SessionLocal()
        try:
            result = db.execute(text("SELECT 1 as test, VERSION() as version"))
            row = result.fetchone()

            return True, {
                "test": row[0] if row else None,
                "version": row[1] if row and len(row) > 1 else None
            }
        finally:
            db.close()

    except Exception as e:
        return False, str(e)


async def test_async_database_connection() -> Tuple[bool, Any]:
    """Test asynchronous database connection"""
    try:
        from app.db.session import get_async_db

        async for db in get_async_db():
            # AsyncSession에서는 await를 사용해야 함
            result = await db.execute(text("SELECT 1 as test, VERSION() as version"))
            row = result.fetchone()  # fetchone()은 동기 메서드

            return True, {
                "test": row[0] if row else None,
                "version": row[1] if row and len(row) > 1 else None
            }

    except Exception as e:
        return False, str(e)


async def test_database_connection_adaptive() -> Tuple[bool, Any]:
    """Test database connection based on current mode"""
    from app.api.v1.dependencies import get_current_mode

    current_mode = get_current_mode()

    if current_mode == "async":
        return await test_async_database_connection()
    else:
        # Run sync test in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=1) as executor:
            return await loop.run_in_executor(
                executor, test_sync_database_connection
            )


# Database Information Utilities
def get_sync_database_info() -> Dict[str, Any]:
    """Get synchronous database information"""
    try:
        from app.db.base import SessionLocal

        db = SessionLocal()
        try:
            # Get basic database info
            queries = {
                "version": "SELECT VERSION() as version",
                "current_db": "SELECT DATABASE() as current_db",
                "connection_id": "SELECT CONNECTION_ID() as connection_id",
                "user": "SELECT USER() as user",
                "now": "SELECT NOW() as current_time"
            }

            info = {}
            for key, query in queries.items():
                try:
                    result = db.execute(text(query))
                    row = result.fetchone()
                    info[key] = row[0] if row else None
                except Exception as e:
                    info[key] = f"Error: {str(e)}"

            return {
                "status": "success",
                "mode": "sync",
                "info": info
            }

        finally:
            db.close()

    except Exception as e:
        return {
            "status": "error",
            "mode": "sync",
            "error": str(e)
        }


async def get_async_database_info() -> Dict[str, Any]:
    """Get asynchronous database information"""
    try:
        from app.db.session import get_async_db

        async for db in get_async_db():
            # Get basic database info
            queries = {
                "version": "SELECT VERSION() as version",
                "current_db": "SELECT DATABASE() as current_db",
                "connection_id": "SELECT CONNECTION_ID() as connection_id",
                "user": "SELECT USER() as user",
                "now": "SELECT NOW() as current_time"
            }

            info = {}
            for key, query in queries.items():
                try:
                    # AsyncSession에서는 execute에 await 사용
                    result = await db.execute(text(query))
                    row = result.fetchone()  # fetchone()은 동기 메서드
                    info[key] = row[0] if row else None
                except Exception as e:
                    info[key] = f"Error: {str(e)}"

            return {
                "status": "success",
                "mode": "async",
                "info": info
            }

    except Exception as e:
        return {
            "status": "error",
            "mode": "async",
            "error": str(e)
        }


async def get_database_info_adaptive() -> Dict[str, Any]:
    """Get database information based on current mode"""
    from app.api.v1.dependencies import get_current_mode

    current_mode = get_current_mode()

    if current_mode == "async":
        return await get_async_database_info()
    else:
        # Run sync function in thread pool
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=1) as executor:
            return await loop.run_in_executor(
                executor, get_sync_database_info
            )


# Database Performance Testing
def run_sync_database_performance_test(query_count: int = 10) -> Dict[str, Any]:
    """Run synchronous database performance test"""
    import time

    try:
        from app.db.base import SessionLocal

        results = []
        start_time = time.time()

        for i in range(query_count):
            query_start = time.time()

            db = SessionLocal()
            try:
                result = db.execute(text("SELECT 1"))
                row = result.fetchone()
                success = row is not None
            except Exception as e:
                print(f"Query {i + 1} failed: {str(e)}")
                success = False
            finally:
                db.close()

            query_time = time.time() - query_start
            results.append({
                "query_number": i + 1,
                "execution_time": query_time,
                "success": success
            })

        total_time = time.time() - start_time
        successful_queries = [r for r in results if r["success"]]

        return {
            "mode": "sync",
            "total_queries": query_count,
            "successful_queries": len(successful_queries),
            "failed_queries": query_count - len(successful_queries),
            "total_time": total_time,
            "average_time": sum(r["execution_time"] for r in results) / len(results),
            "queries_per_second": query_count / total_time if total_time > 0 else 0,
            "results": results
        }

    except Exception as e:
        return {
            "mode": "sync",
            "error": str(e),
            "status": "error"
        }


async def run_async_database_performance_test(query_count: int = 10) -> Dict[str, Any]:
    """Run asynchronous database performance test"""
    import time

    try:
        from app.db.session import get_async_db

        results = []
        start_time = time.time()

        for i in range(query_count):
            query_start = time.time()

            try:
                async for db in get_async_db():
                    # AsyncSession에서는 execute에 await 사용
                    result = await db.execute(text("SELECT 1"))
                    row = result.fetchone()
                    success = row is not None
                    break
            except Exception as e:
                print(f"Query {i + 1} failed: {str(e)}")
                success = False

            query_time = time.time() - query_start
            results.append({
                "query_number": i + 1,
                "execution_time": query_time,
                "success": success
            })

        total_time = time.time() - start_time
        successful_queries = [r for r in results if r["success"]]

        return {
            "mode": "async",
            "total_queries": query_count,
            "successful_queries": len(successful_queries),
            "failed_queries": query_count - len(successful_queries),
            "total_time": total_time,
            "average_time": sum(r["execution_time"] for r in results) / len(results),
            "queries_per_second": query_count / total_time if total_time > 0 else 0,
            "results": results
        }

    except Exception as e:
        return {
            "mode": "async",
            "error": str(e),
            "status": "error"
        }


async def run_database_performance_test_adaptive(query_count: int = 10) -> Dict[str, Any]:
    """Run database performance test based on current mode"""
    from app.api.v1.dependencies import get_current_mode

    current_mode = get_current_mode()

    if current_mode == "async":
        return await run_async_database_performance_test(query_count)
    else:
        # Run sync test in thread pool
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=1) as executor:
            return await loop.run_in_executor(
                executor, run_sync_database_performance_test, query_count
            )


# Database Table Information
def get_sync_table_info() -> Dict[str, Any]:
    """Get table information synchronously"""
    try:
        from app.db.base import SessionLocal  # 수정: import 경로

        db = SessionLocal()
        try:
            # Get table information
            result = db.execute(text("""
                SELECT TABLE_NAME, TABLE_ROWS, DATA_LENGTH, INDEX_LENGTH, CREATE_TIME
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                ORDER BY TABLE_NAME
            """))

            tables = []
            for row in result:
                tables.append({
                    "name": row[0],
                    "rows": row[1] if row[1] is not None else 0,
                    "data_size_bytes": row[2] if row[2] is not None else 0,
                    "index_size_bytes": row[3] if row[3] is not None else 0,
                    "created_time": str(row[4]) if row[4] is not None else None
                })

            return {
                "status": "success",
                "mode": "sync",
                "database": settings.db_name,
                "total_tables": len(tables),
                "tables": tables
            }

        finally:
            db.close()

    except Exception as e:
        return {
            "status": "error",
            "mode": "sync",
            "error": str(e)
        }


async def get_async_table_info() -> Dict[str, Any]:
    """Get table information asynchronously"""
    try:
        from app.db.session import get_async_db  # 수정: import 경로

        async for db in get_async_db():
            # Get table information
            result = await db.execute(text("""
                SELECT TABLE_NAME, TABLE_ROWS, DATA_LENGTH, INDEX_LENGTH, CREATE_TIME
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                ORDER BY TABLE_NAME
            """))

            tables = []
            for row in result:
                tables.append({
                    "name": row[0],
                    "rows": row[1] if row[1] is not None else 0,
                    "data_size_bytes": row[2] if row[2] is not None else 0,
                    "index_size_bytes": row[3] if row[3] is not None else 0,
                    "created_time": str(row[4]) if row[4] is not None else None
                })

            return {
                "status": "success",
                "mode": "async",
                "database": settings.db_name,
                "total_tables": len(tables),
                "tables": tables
            }

    except Exception as e:
        return {
            "status": "error",
            "mode": "async",
            "error": str(e)
        }


async def get_table_info_adaptive() -> Dict[str, Any]:
    """Get table information based on current mode"""
    from app.api.v1.dependencies import get_current_mode

    current_mode = get_current_mode()

    if current_mode == "async":
        return await get_async_table_info()
    else:
        # Run sync function in thread pool
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=1) as executor:
            return await loop.run_in_executor(
                executor, get_sync_table_info
            )
