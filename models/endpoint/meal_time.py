from pydantic import BaseModel
from models.endpoint.meal import Meal


class MealTime(BaseModel):
    breakfast: list[Meal] = list()
    lunch: list[Meal] = list()
    dinner: list[Meal] = list()
