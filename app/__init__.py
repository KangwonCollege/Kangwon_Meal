import sqlalchemy
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import get_settings
from app.db.base import Base
from app.utils.import_supporter import ImportSupporter

BASE_DIR = Path(__file__).parent.parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    if settings.use_sqlite:
        engine = create_async_engine(
            f"sqlite+aiosqlite:///{settings.db_path}",
            connect_args={"check_same_thread": False},
        )
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    else:
        engine = create_async_engine(
            sqlalchemy.engine.url.URL.create(
                drivername="mysql+aiomysql",
                username=settings.db_user,
                host=settings.db_host,
                password=settings.db_password,
                database=settings.db_name,
                port=settings.db_port,
            )
        )

    app.state.session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

ImportSupporter(app).load_routers("app.api", str(BASE_DIR))
