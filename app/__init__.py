import sqlalchemy
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import get_settings
from app.db.base import Base
from app.utils.import_supporter import ImportSupporter

BASE_DIR = Path(__file__).parent.parent


def _build_engine(settings):
    if settings.use_sqlite:
        return create_async_engine(
            f"sqlite+aiosqlite:///{settings.db_path}",
            connect_args={"check_same_thread": False},
        )

    if settings.use_cloud_sql:
        url = sqlalchemy.engine.url.URL.create(
            drivername="mysql+aiomysql",
            username=settings.db_user,
            password=settings.db_password,
            database=settings.db_name,
            query={"unix_socket": f"/cloudsql/{settings.cloud_sql_instance}"},
        )
    else:
        url = sqlalchemy.engine.url.URL.create(
            drivername="mysql+aiomysql",
            username=settings.db_user,
            host=settings.db_host,
            password=settings.db_password,
            database=settings.db_name,
            port=settings.db_port,
        )

    return create_async_engine(url)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    engine = _build_engine(settings)

    if settings.use_sqlite:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    app.state.session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

ImportSupporter(app).load_routers("app.api", str(BASE_DIR))
