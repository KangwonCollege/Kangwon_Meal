import datetime

from sqlalchemy import Date, Enum
from sqlalchemy.orm import relationship, mapped_column, Mapped

from models.building import Building
from models.database.restaurant import Restaurant
from models.dormitory_response import DormitoryResponse
from models.meal_response import MealResponse
from models.enumeration.meal_type import MealType
from .base import Base


class MealInfo(Base):
    __tablename__ = "meal_info"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[datetime.date] = mapped_column(Date)
    building = mapped_column(Enum(Building))

    breakfast: Mapped[list["Restaurant"]] = relationship(
        primaryjoin="and_(MealInfo.id==Restaurant.parent_id, " "Restaurant.type=='breakfast')")
    lunch: Mapped[list["Restaurant"]] = relationship(
        primaryjoin="and_(MealInfo.id==Restaurant.parent_id, " "Restaurant.type=='lunch')")
    dinner: Mapped[list["Restaurant"]] = relationship(
        primaryjoin="and_(MealInfo.id==Restaurant.parent_id, " "Restaurant.type=='dinner')")
    
    @classmethod
    def _from_dormitory(cls, date: datetime.date, building: Building, data: MealResponse):
        new_cls = cls(
            date=date,
            building=building
        )
        if data.breakfast is not None and "미운영" not in data.breakfast:
            new_cls.breakfast.append(
                Restaurant.from_data(meal_type=MealType.breakfast, meal=data.breakfast)
            )
        if data.lunch is not None and "미운영" not in data.lunch:
            new_cls.lunch.append(
                Restaurant.from_data(meal_type=MealType.lunch, meal=data.lunch)
            )
        if data.dinner is not None and "미운영" not in data.dinner:
            new_cls.dinner.append(
                Restaurant.from_data(meal_type=MealType.dinner, meal=data.dinner)
            )
        return new_cls
    
    @classmethod
    def from_dormitory(cls, date: datetime.date, data: DormitoryResponse):
        return [
            cls._from_dormitory(date, Building.dorm_1, data.BTL1),
            cls._from_dormitory(date, Building.dorm_2, data.BTL2)
        ]
