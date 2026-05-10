from pydantic import BaseModel


class MealResponse(BaseModel):
    breakfast: list[str] | None = None
    lunch: list[str] | None = None
    dinner: list[str] | None = None
