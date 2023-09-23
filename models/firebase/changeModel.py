import datetime
import asyncio

from models.firebase.mealModel import MealModel
from models.firebase.baseFirebase import BaseFirebase
from modules.meal.schoolMealType import SchoolMealType
from modules.meal.schoolMeal import SchoolMeal
from modules.meal.dormitoryMeal import DormitoryMeal
from modules.meal.mealResponse import MealResponse
from modules.meal.dormitoryResponse import DormitoryResponse


class ChangeModel(BaseFirebase):
    def __init__(self, loop: asyncio.AbstractEventLoop):
        super(ChangeModel).__init__(loop)
        self.data: MealModel | None = None

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

    async def change_model(self, date: datetime.date = datetime.date.today()) -> MealModel:
        school_meal = await ChangeModel.load_school_meal()
        dorm_meal = await ChangeModel.load_dorm_meal()

        return self.data
