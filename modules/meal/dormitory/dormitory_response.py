from pydantic import BaseModel

from .meal_response import MealResponse


class DormitoryResponse(BaseModel):
    general: MealResponse = MealResponse()
    BTL1: MealResponse = MealResponse()
    BTL2: MealResponse = MealResponse()
