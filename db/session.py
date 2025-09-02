from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import Optional, AsyncGenerator
from core import settings

engine: Optional[AsyncEngine] = None
async_session: Optional[sessionmaker] = None

def init_db_engine(
        database_url: str = settings.DATABASE_URL,
        *,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: int = 30,
        pool_recycle: int = 1800,
        echo: bool = False,
) -> AsyncEngine:
    global engine, async_session

    if engine is not None:
        return engine
    
    engine = create_async_engine(
        database_url,
        echo=echo,
        future=True,
        pool_size= pool_size,
        max_overflow= max_overflow,
        pool_timeout= pool_timeout,
        pool_recycle= pool_recycle
    )

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    return engine

def get_db_engine() -> AsyncEngine:
    if engine is None:
        raise RuntimeError("DB engine not initialized, call init_db_engine first")
    return engine

async def shutdown_db() -> None:
    global engine, async_session
    if engine is not None:
        await engine.dispose()
        engine = None
        async_session = None

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if async_session is None:
        raise RuntimeError("DB engine is not initialized, call init_db_engine first")
    async with async_session() as session:
        yield session
