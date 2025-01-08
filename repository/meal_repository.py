import datetime
from typing import Sequence

from sqlalchemy.sql import select, exists

from models.building import Building
from models.database import MealInfo
from repository.base_repository import BaseRepository


class MealRepository(BaseRepository):
    async def meal(
            self,
            building: list[Building],
            date: datetime.date
    ) -> Sequence[MealInfo]:
        query = select(MealInfo).where(MealInfo.date == date).where(MealInfo.building.in_(building))
        result = await self._session.execute(query)
        return result.scalars().all()

    async def meal_exist(
            self,
            building: Building,
            date: datetime.date
    ) -> bool:
        query = select(exists(MealInfo).where(MealInfo.date == date).where(MealInfo.building == building))
        result = await self._session.execute(query)
        return result.scalar_one()