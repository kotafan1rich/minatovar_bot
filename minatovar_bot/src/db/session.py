from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.config import get_postgres_url, settings

engine = create_async_engine(url=get_postgres_url(), future=True, echo=settings.DEBUG)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator:
    session: AsyncSession = async_session()
    try:
        yield session
    finally:
        await session.close()
