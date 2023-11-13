from pydantic import BaseModel


class Meal(BaseModel):
    name: str | None
    meal: list[str]
