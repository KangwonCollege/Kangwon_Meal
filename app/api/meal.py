import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.meal_info import MealInfo
from app.db.repositories.meal import MealRepository
from app.db.session import get_session
from app.models.building import Building
from app.models.schemas.meal_info import MealInfo as MealInfoSchema
from app.services.dormitory_meal import DormitoryMeal
from app.services.school_meal import SchoolMeal

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("/", response_model=list[MealInfoSchema])
async def get_meal(
    building: str = None,
    date: datetime.date = None,
    session: SessionDep = None,
):
    if date is None:
        date = datetime.date.today()

    _building_for_filter = []
    if building is not None:
        for key in building.split(','):
            _building_for_filter.append(Building.find_key(key))
    else:
        _building_for_filter = list(Building)

    repo = MealRepository(session)
    dormitory_client = DormitoryMeal()
    school_client = SchoolMeal()
    repository_data = []
    is_dormitory = False

    for _building in _building_for_filter:
        if await repo.meal_exist(_building, date):
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

    await repo.meal_update(repository_data)
    result = await repo.meal(_building_for_filter, date)
    return [await MealInfoSchema.model_validate_sql(x) for x in result]
