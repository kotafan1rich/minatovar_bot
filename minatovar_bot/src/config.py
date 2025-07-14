import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""
    DEBUG: bool
    TOKEN: str
    HOST: str
    PORT: int
    WEBHOOK_PATH: str = '/webhook'
    BASE_URL: str

    REDIS_PORT: int
    REDIS_HOST: str
    REDIS_DB: int
    REDIS_PASSWORD: str
    REDIS_USER: str

    STATIC_FILES: str = "static"
    TEMPLATE_DIR: str = "src/templates"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_NAME: str
    POSTGRES_PORT: int
    POSTGRES_HOST: str
    SECRET_KEY: str

    ADMIN_GROUP_ID: int = -4745215109

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()

ADMINS = (1019030670, 1324716819, 1423930901)
LOG_ADMIN = 1324716819

def get_media_files() -> str:
    """Returns the path to the media files directory."""
    return f"{settings.STATIC_FILES}/media"

def get_postgres_url() -> str:
    """Returns the PostgreSQL database URL for async operations."""
    return f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_NAME}"


def get_alembic_db_url() -> str:
    """Returns the PostgreSQL database URL for Alembic migrations."""
    return f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_NAME}"


def get_redis_url() -> str:
    """Returns the Redis database URL."""
    return f"redis://{settings.REDIS_USER}:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
