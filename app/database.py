import asyncio
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
    pool_size=5,
    max_overflow=10
)

async def get_session() -> AsyncSession:
    async with AsyncSession(async_engine) as session, session.begin():
        yield session


session_dep = Depends(get_session)
SessionDep = Annotated[AsyncSession, session_dep]
get_session = asynccontextmanager(get_session)

# with sync_engine.connect() as conn:
#     res = conn.execute(text("SELECT 1,2,3 union 4,5,6"))
#     print(f"{res.first()=}")