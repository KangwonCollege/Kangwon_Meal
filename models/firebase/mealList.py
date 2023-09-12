from pydantic import BaseModel


class MealList(BaseModel):
    name: str | None = None
    meal: list[str] | None = None
