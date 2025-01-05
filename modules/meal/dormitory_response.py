from pydantic import BaseModel
from modules.meal.mealResponse import MealResponse


class DormitoryResponse(BaseModel):
    general: MealResponse = MealResponse()
    BTL1: MealResponse = MealResponse()
    BTL2: MealResponse = MealResponse()
