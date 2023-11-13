import datetime

from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from models.building import Building
from models.endpoint import MealInfo as MealInfoEndpoint
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

    result = await session.get_meal(_building_for_fliter, date)
    return result


def setup(client: FastAPI, _db: async_sessionmaker):
    global database
    database.set_factory(_db)
    client.include_router(router)
