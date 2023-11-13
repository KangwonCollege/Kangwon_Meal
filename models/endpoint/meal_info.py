import datetime

from pydantic import BaseModel
from models.endpoint.meal_time import MealTime


class MealInfo(BaseModel):
    building: str
    date: datetime.date
    meal: MealTime
