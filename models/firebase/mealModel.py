from pydantic import BaseModel


class MealInfo(BaseModel):
    name: str | None = None
    meal: list[str] | None


class MealInfoModel(BaseModel):
    breakfast: list[MealInfo] | None = None
    lunch: list[MealInfo] | None = None
    dinner: list[MealInfo] | None = None


class MealModel(BaseModel):
    date: str
    building: str
    meal: MealInfoModel | None = None


if __name__ == "__main__":
    print(MealModel(
        date="2",
        building="s",
        meal=MealInfoModel(breakfast=MealInfo(meal=["test,", "test2"]))
    ).model_dump_json(indent=4))

    data = {"test": 1, "test2": 2}

    print(len(data))
    for key, data in enumerate(data):
        print(key, data)
