from pydantic import BaseModel
from modules.mealTimeModel.mealType import MealType


class Week(BaseModel):
    weekday: MealType | None = None
    weekend_saturday: MealType | None = None
    weekend_sunday: MealType | None = None
