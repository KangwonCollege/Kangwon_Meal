import datetime
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, exists

from app.db.models.meal_info import MealInfo
from app.models.building import Building


class MealRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def meal(self, building: list[Building], date: datetime.date) -> Sequence[MealInfo]:
        query = select(MealInfo).where(MealInfo.date == date).where(MealInfo.building.in_(building))
        result = await self._session.execute(query)
        return result.scalars().all()

    async def meal_exist(self, building: Building, date: datetime.date) -> bool:
        query = select(exists(MealInfo).where(MealInfo.date == date).where(MealInfo.building == building))
        result = await self._session.execute(query)
        return result.scalar_one()

    async def meal_update(self, data: Sequence[MealInfo]):
        self._session.add_all(data)
        await self._session.commit()
