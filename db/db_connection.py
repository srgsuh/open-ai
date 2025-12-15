from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy import URL
import urllib.parse
from configuration import get_config_parameter

def build_engine() -> AsyncEngine:
    db_url: URL = URL.create(
        "postgresql+asyncpg",
        username=get_config_parameter("POSTGRES_USER"),
        password=urllib.parse.quote_plus(get_config_parameter("POSTGRES_PASSWORD")),  # plain (unescaped) text
        host=get_config_parameter("POSTGRES_HOST"),
        database=get_config_parameter("POSTGRES_DB"),
        port=int(get_config_parameter("POSTGRES_PORT"))
    )
    engine: AsyncEngine = create_async_engine(db_url)

    return engine

engine: AsyncEngine = build_engine()