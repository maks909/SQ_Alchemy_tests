import asyncio
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10
)

with sync_engine.connect() as conn:
    res = conn.execute(text("SELECT 1,2,3 union 4,5,6"))
    print(f"{res.first()=}")