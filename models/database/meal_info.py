import datetime

from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Column, Integer, Date, Enum
from typing import TYPE_CHECKING

from .base import Base
from models.building import Building
from models.meal_type import MealType
from models.database.meal import Meal


class MealInfo(Base):
    __tablename__ = "meal_info"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date)
    building = mapped_column(Enum(Building))

    breakfast: Mapped[list["Meal"]] = relationship(primaryjoin="and_(MealInfo.id==Meal.parent_id, " "Meal.type=='breakfast')")
    lunch: Mapped[list["Meal"]] = relationship(primaryjoin="and_(MealInfo.id==Meal.parent_id, " "Meal.type=='lunch')")
    dinner: Mapped[list["Meal"]] = relationship(primaryjoin="and_(MealInfo.id==Meal.parent_id, " "Meal.type=='dinner')")
