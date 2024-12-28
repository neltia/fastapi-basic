from fastapi import FastAPI
from routers.users import user_router
from routers.products import product_router
from routers.admin import admin_router

app = FastAPI()
app.include_router(user_router)
app.include_router(product_router)
app.include_router(admin_router)
