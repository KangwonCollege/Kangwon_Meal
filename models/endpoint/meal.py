from pydantic import BaseModel
from models.database.restaurant import Restaurant


class Meal(BaseModel):
    name: str | None
    meal: list[str]

    @classmethod
    async def model_validate_sql(cls, data: Restaurant):
        meal = await data.awaitable_attrs.meal
        return cls(name=data.name, meal=[x.name for x in meal])
