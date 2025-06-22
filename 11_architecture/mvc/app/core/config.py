from pydantic import Field, field_validator
from pydantic_settings import BaseSettings as PydanticSettings
from typing import Optional


class Settings(PydanticSettings):
    # Database Configuration
    db_host: str = Field(..., env="DB_HOST")
    db_port: int = Field(3306, env="DB_PORT")
    db_user: str = Field(..., env="DB_USER")
    db_password: str = Field(..., env="DB_PASSWORD")
    db_name: str = Field(..., env="DB_NAME")

    async_mode: bool = True
    database_url: Optional[str] = Field(None, env="DATABASE_URL")
    database_async_url: Optional[str] = Field(None, env="DATABASE_ASYNC_URL")

    database_pool_size: int = Field(5, env="DB_POOL_SIZE")
    database_max_overflow: int = Field(10, env="DB_MAX_OVERFLOW")

    # Application Configuration
    app_name: str = Field("FastAPI Users API", env="APP_NAME")
    app_version: str = Field("1.0.0", env="APP_VERSION")
    debug: bool = Field(False, env="DEBUG")

    # Security
    secret_key: str = Field(..., env="SECRET_KEY")

    # Redis Configuration
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
