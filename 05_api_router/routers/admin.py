from fastapi import APIRouter

admin_router = APIRouter(prefix="/admin", tags=["admin"])


@admin_router.get("/dashboard")
def admin_dashboard():
    return {"message": "Welcome to the Admin Dashboard"}


@admin_router.get("/stats")
def admin_stats():
    return {"users": 10, "products": 5, "sales": 20}
