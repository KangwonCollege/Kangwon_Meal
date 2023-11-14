from pydantic import BaseModel

from models.database.meal_info import MealInfo
from models.endpoint.meal import Meal


class MealTime(BaseModel):
    breakfast: list[Meal] = list()
    lunch: list[Meal] = list()
    dinner: list[Meal] = list()

    @classmethod
    async def model_validate_sql(cls, data: MealInfo):
        key = ("breakfast", "lunch", "dinner")
        _data = {}
        for k in key:
            _data[k] = [
                await Meal.model_validate_sql(x)
                for x in await getattr(data.awaitable_attrs, k)
            ]
        return cls(**_data)
