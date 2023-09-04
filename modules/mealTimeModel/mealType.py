from pydantic import BaseModel
from modules.mealTimeModel.operatingTime import OperatingTime


class MealType(BaseModel):
    breakfast: OperatingTime | None = None
    lunch: OperatingTime | None = None
    dinner: OperatingTime | None = None
