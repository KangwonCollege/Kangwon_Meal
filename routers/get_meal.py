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
    for building in _building_for_fliter:
        exist = await session.meal_exist(building, date)
        if exist:
            continue
        
        if building.type == "dormitory":
            dormitory_client = DormitoryMeal(loop=loop)
            await dormitory_client.meal(date=date)
            for date, dormitory_response in dormitory_client.data.items():
                repository_data.extend(
                    MealInfo.from_dormitory(date=date, data=dormitory_response)
                )
            await dormitory_client.close()
        else:
            pass
    # result = await session.meal(_building_for_fliter, date)
    return [await MealInfoEndpoint.model_validate_sql(x) for x in repository_data]


def setup(client: FastAPI, _db: async_sessionmaker):
    global database
    database.set_factory(_db)
    client.include_router(router)
