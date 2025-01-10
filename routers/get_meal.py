import asyncio
import datetime

from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from models.building import Building
from models.database import MealInfo
from models.endpoint import MealInfo as MealInfoEndpoint
from modules.dormitory_meal import DormitoryMeal
from modules.school_meal import SchoolMeal
from repository.meal_repository import MealRepository

router = APIRouter()
database = MealRepository()


@router.get("/", response_model=list[MealInfoEndpoint])
async def get_meal(
        building: str = None,
        date: datetime.date = None,
        session: MealRepository = Depends(database.call)
):
    if date is None:
        date = datetime.date.today()
    _building_for_fliter = []
    if building is not None:
        for key in building.split(','):
            _building_for_fliter.append(Building.find_key(key))
    else:
        _building_for_fliter = list(Building)

    loop = asyncio.get_running_loop()
    repository_data = []
    is_dormitory = False
    
    dormitory_client = DormitoryMeal(loop=loop)
    school_client = SchoolMeal(loop=loop)
    for _building in _building_for_fliter:
        exist = await session.meal_exist(_building, date)
        if exist:
            continue
        
        if _building.type == "dormitory" and not is_dormitory:
            is_dormitory = True
            await dormitory_client.meal(date=date)
            for _date, dormitory_response in dormitory_client.data.items():
                repository_data.extend(
                    MealInfo.from_dormitory(date=_date, data=dormitory_response)
                )
        elif _building.type == "school":
            await school_client.meal(date=date, building=_building.school_meal_type)
            for _date, school_response in school_client.data[_building.school_meal_type].items():
                repository_data.append(
                    MealInfo.from_school(date=_date, building=_building, data=school_response)
                )
    await dormitory_client.close()
    await school_client.close()
    
    await session.meal_update(repository_data)
    result = await session.meal(_building_for_fliter, date)
    return [await MealInfoEndpoint.model_validate_sql(x) for x in result]


def setup(client: FastAPI, _db: async_sessionmaker):
    global database
    database.set_factory(_db)
    client.include_router(router)
