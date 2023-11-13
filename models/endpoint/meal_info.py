import datetime

from pydantic import BaseModel

from models.building import Building
from models.endpoint.meal_time import MealTime
from models.database import MealInfo as MealInfoDB


class MealInfo(BaseModel):
    building: Building
    date: datetime.date
    meal: MealTime

    @classmethod
    async def model_validate_sql(cls, data: MealInfoDB):
        meal_time = await MealTime.model_validate_sql(data)
        return cls(building=data.building, date=data.date, meal=meal_time)
