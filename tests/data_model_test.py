import asyncio
import datetime

import sqlalchemy
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncConnection
from sqlalchemy.sql import select

from config.config import get_config
from models.building import Building
from models.meal_type import MealType
from models.database.meal import Meal
from models.database.meal_info import MealInfo

database_parser = get_config()
database_section = database_parser.get("Default", "database_section")
database = {
    "drivername": "mysql+aiomysql",
    "username": database_parser.get(database_section, "user"),
    "host": database_parser.get(database_section, "host"),
    # "password": database_parser.get(database_section, "password"),
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

sample_data = {
    "date": datetime.date.today(),
    "building": Building.cheonji,
    "meal": {
        "breakfast": [
            {
                "name": "천원의 아침밥",
                "meal": ["왕감자", "왕감자"],
            },
            {
                "name": "맛있는 아침밥",
                "meal": ["왕감자", "왕감자"],
            }
        ],
        "lunch": [
            {
                "name": "맛있는 점심",
                "meal": ["왕감자", "왕감자"],
            },
            {
                "name": "맛깔나는 점심",
                "meal": ["왕감자", "왕감자"],
            }
        ],
        "dinner": [
            {
                "name": "맛있는 저녁",
                "meal": ["왕감자", "왕감자"],
            },
            {
                "name": "맛깔나는 저녁",
                "meal": ["왕감자", "왕감자"],
            }
        ]
    }

}


async def main():
    async with engine.begin() as conn:
        conn: AsyncConnection
        await conn.run_sync(MealInfo.metadata.create_all)
        await conn.run_sync(Meal.metadata.create_all)
        await conn.commit()

    async with factory() as session:
        """async with session.begin():
            info = MealInfo(
                    date=datetime.date.today(),
                    building=Building.cheonji
                )
            info.dinner.append(
                Meal(name="밥", type=MealType.dinner)
            )
            info.dinner.append(
                Meal(name="국", type=MealType.dinner)
            )
            info.dinner.append(
                Meal(name="토스트", type=MealType.breakfast)
            )
            session.add(info)"""

        result = await session.execute(select(MealInfo).order_by(MealInfo.id))

        a1: MealInfo = result.scalars().one()

        print(a1.date)
        print("breakfest", (await a1.awaitable_attrs.breakfast)[0].name)
        print("lunch", await a1.awaitable_attrs.lunch)
        print("dinner:", await a1.awaitable_attrs.dinner)

    await engine.dispose()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
