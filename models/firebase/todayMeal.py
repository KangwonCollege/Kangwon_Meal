from mealList import MealList
from pydantic import BaseModel


class TodayMeal(BaseModel):
    breakfast: list[MealList] | None = None
    lunch: list[MealList] | None = None
    dinner: list[MealList] | None = None
