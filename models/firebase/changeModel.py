import datetime
import asyncio

from models.firebase.mealModel import MealModel, MealInfoModel, MealInfo
from models.firebase.baseFirebase import BaseFirebase
from modules.meal.schoolMealType import SchoolMealType
from modules.meal.schoolMeal import SchoolMeal
from modules.meal.dormitoryMeal import DormitoryMeal
from modules.meal.mealResponse import MealResponse
from modules.meal.dormitoryResponse import DormitoryResponse


class ChangeModel(BaseFirebase):
    def __init__(self, loop: asyncio.AbstractEventLoop):
        super(ChangeModel, self).__init__(loop=loop)
        self.change_school_meal: MealModel | None = None

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
    ) -> MealModel:
        if building is None:
            raise Exception("building is None.")
        if school_meal is None:
            school_meal = await ChangeModel.load_school_meal(date=date, building=building)

        meal_model = MealModel(
            date=str(date),
            building=str(building.value),
            meal=MealInfoModel()
        )

        meal_info_breakfast, meal_info_lunch, meal_info_dinner = [], [], []
        for i, name in enumerate(school_meal):
            if school_meal[name].breakfast is None:
                pass
            else:
                meal_info_breakfast.append(MealInfo(name=name, meal=school_meal[name].breakfast))
            if school_meal[name].lunch is None:
                pass
            else:
                meal_info_lunch.append(MealInfo(name=name, meal=school_meal[name].lunch))
            if school_meal[name].dinner is None:
                pass
            else:
                meal_info_dinner.append(MealInfo(name=name, meal=school_meal[name].dinner))
        meal_model.meal = MealInfoModel(
            breakfast=meal_info_breakfast,
            lunch=meal_info_lunch,
            dinner=meal_info_dinner
        )

        self.change_school_meal = meal_model

        return self.change_school_meal

    async def change_dorm_model(
            self,
            date: datetime.date = datetime.date.today()
    ) -> MealModel:
        pass
