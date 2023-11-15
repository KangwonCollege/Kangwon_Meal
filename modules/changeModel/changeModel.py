import datetime
import asyncio

from modules.changeModel.mealInfoModel import MealInfoModel, MealTimeModel, MealModel
from modules.meal.schoolMealType import SchoolMealType
from modules.meal.schoolMeal import SchoolMeal
from modules.meal.dormitoryMeal import DormitoryMeal
from modules.meal.mealResponse import MealResponse
from modules.meal.dormitoryResponse import DormitoryResponse
from modules.meal.dormitoryMealType import DomitoryMealType
from modules.meal.baseMeal import BaseMeal


class ChangeModel(BaseMeal):
    def __init__(self, loop: asyncio.AbstractEventLoop):
        super(ChangeModel, self).__init__(loop=loop)
        self.change_school_meal: MealInfoModel | None = None

    @staticmethod
    async def load_school_meal(
            building: SchoolMealType = None,
            date: datetime.date = datetime.date.today()
    ) -> dict[str, MealResponse]:
        school_meal = SchoolMeal(loop=asyncio.get_event_loop())
        school_meal_data = await school_meal.meal(
            building=building,
            date=date
        )
        return school_meal_data

    @staticmethod
    async def load_dorm_meal(date: datetime.date = datetime.date.today()) -> DormitoryResponse:
        dorm_meal = DormitoryMeal(loop=asyncio.get_event_loop())
        dorm_meal_data = await dorm_meal.meal(date=date)
        return dorm_meal_data

    async def change_school_model(
            self,
            date: datetime.date = datetime.date.today(),
            building: SchoolMealType | None = None,
            school_meal: dict | SchoolMeal | None = None
    ) -> MealInfoModel:
        if building is None:
            raise Exception("building is None.")
        if school_meal is None:
            school_meal = await self.load_school_meal(date=date, building=building)

        meal_model = MealInfoModel(
            date=str(date),
            building=str(building.value),
            meal=MealTimeModel()
        )

        meal_info_breakfast, meal_info_lunch, meal_info_dinner = [], [], []
        for i, name in enumerate(school_meal):
            meal_info_breakfast.append(MealModel(name=name, meal=school_meal[name].breakfast))
            meal_info_lunch.append(MealModel(name=name, meal=school_meal[name].lunch))
            meal_info_dinner.append(MealModel(name=name, meal=school_meal[name].dinner))

        meal_model.meal = MealTimeModel(
            breakfast=meal_info_breakfast,
            lunch=meal_info_lunch,
            dinner=meal_info_dinner
        )

        return meal_model

    async def change_dorm_model(
            self,
            date: datetime.date = datetime.date.today()
    ) -> MealInfoModel:
        meal_models = []

        dorm_data = await self.load_dorm_meal()

        for i, meal_data in enumerate(dorm_data):
            meal_model = MealInfoModel(
                date=str(date),
                building=str(DomitoryMealType(i).name),
                meal=MealTimeModel()
            )
            # print(meal_data)

            meal_model.meal = MealTimeModel(
                breakfast=[(MealModel(name=None, meal=meal_data[1].breakfast))],
                lunch=[(MealModel(name=None, meal=meal_data[1].lunch))],
                dinner=[(MealModel(name=None, meal=meal_data[1].dinner))]
            )
            meal_models.append(meal_model)

        return meal_models
