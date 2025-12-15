from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    AsyncSession,
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
    engine: AsyncEngine = create_async_engine(db_url, echo=True,future=True)

    return engine

engine: AsyncEngine = build_engine()

session_maker: async_sessionmaker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)