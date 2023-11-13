from pydantic import BaseModel
from models.endpoint.meal import Meal


class MealTime(BaseModel):
    breakfast: list[Meal]
    lunch: list[Meal]
    dinner: list[Meal]
