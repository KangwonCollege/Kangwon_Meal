import logging
import sqlalchemy

from fastapi import FastAPI
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config.config import get_config
from utils.directory import directory
from utils.import_supporter import ImportSupporter

app = FastAPI()
log = logging.getLogger(__name__)

# Database
database_parser = get_config()
database_section = database_parser.get("Default", "database_section")
database = {
    "drivername": "mysql+aiomysql",
    "username": database_parser.get(database_section, "user"),
    "host": database_parser.get(database_section, "host"),
    "password": database_parser.get(database_section, "password"),
    "database": database_parser.get(database_section, "database"),
    "port": database_parser.getint(database_section, "port", fallback=3306),
}
database_url = sqlalchemy.engine.url.URL.create(
    **database
)
engine = create_async_engine(
    database_url,
    poolclass=NullPool,
)
factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

view_image_supporter = ImportSupporter(app, factory)

view_image_supporter.load_modules('routers', directory)
