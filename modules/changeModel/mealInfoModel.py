from pydantic import BaseModel


class MealModel(BaseModel):
    name: str | None = None
    meal: list[str] | None


class MealTimeModel(BaseModel):
    breakfast: list[MealModel] | None = None
    lunch: list[MealModel] | None = None
    dinner: list[MealModel] | None = None


class MealInfoModel(BaseModel):
    date: str
    building: str
    meal: MealTimeModel | None = None


if __name__ == "__main__":
    print(MealInfoModel(
        date="2",
        building="s",
        meal=MealTimeModel(breakfast=[MealModel(name="test11", meal=["test,", "test2"])], lunch=None, dinner=None)
    ).model_dump_json(indent=4))

    data = {"test": 1, "test2": 2}

    print(len(data))
    for key, data in enumerate(data):
        print(key, data)
