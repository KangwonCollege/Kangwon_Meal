from pydantic import BaseModel


class _MealInfo(BaseModel):
    name: int | None = None
    meal: list[str]


class _MealInfoModel(BaseModel):
    breakfast: _MealInfo | None
    lunch: _MealInfo | None
    dinner: _MealInfo | None


class MealModel(BaseModel):
    date: str
    building: str
    meal: _MealInfoModel | None = None
