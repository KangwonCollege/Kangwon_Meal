from todayMeal import TodayMeal
from pydantic import BaseModel


class MealDatabase(BaseModel):
    date: str = None
    building: str = None
    meal: TodayMeal = TodayMeal()
