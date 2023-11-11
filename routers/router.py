from fastapi import FastAPI
import sqlalchemy
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from datetime import datetime

from utils.getConfig import get_config


app = FastAPI()


@app.on_event("startup")
async def startup():
    # Database
    database_parser = get_config(config_name="token")
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
    
    print("==========DB Connect==========")


@app.on_event("shutdown")
async def shutdown():
    print("==========DB Disconnect==========")


@app.get("/")
async def ping():
    print("main point")
    return {"respone": "pong"}


@app.get("/")
async def get_meal(building: str, date: datetime):
    return {
        "meal": "a",
        "building": building,
        "date": date
    }
