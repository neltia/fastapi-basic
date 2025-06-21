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

    database_url: Optional[str] = Field(None, env="DATABASE_URL")

    # Application Configuration
    app_name: str = Field("FastAPI Users API", env="APP_NAME")
    app_version: str = Field("1.0.0", env="APP_VERSION")
    debug: bool = Field(False, env="DEBUG")

    # Security
    secret_key: str = Field(..., env="SECRET_KEY")

    # Redis Configuration
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")

    @field_validator('database_url')
    @classmethod
    def build_database_url(cls, v, info):
        """Build database URL from individual components if not provided"""
        if v:
            return v
        values = info.data

        # Build URL from individual components
        db_host = values.get('db_host')
        db_port = values.get('db_port')
        db_user = values.get('db_user')
        db_password = values.get('db_password')
        db_name = values.get('db_name')

        if all([db_host, db_port, db_user, db_password, db_name]):
            return f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        raise ValueError("Either DATABASE_URL or all individual DB components must be provided")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
