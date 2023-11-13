import datetime

from pydantic import BaseModel, model_validator, field_validator, validator
from typing import Any, TYPE_CHECKING

from models.building import Building
from models.endpoint.meal_time import MealTime
from models.database import MealInfo as MealInfoDB


class MealInfo(BaseModel):
    building: Building
    date: datetime.date
    meal: MealTime = MealTime()

    def __init__(self, **kw):
        print(1)
        super().__init__(**kw)

    @classmethod
    @field_validator("date", mode="wrap")
    def check_meal_validator(cls, data):
        print(1)
        return data
