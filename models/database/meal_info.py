import datetime

from sqlalchemy import Date, Enum
from sqlalchemy.orm import relationship, mapped_column, Mapped

from models.building import Building
from models.database.restaurant import Resaurant
from .base import Base


class MealInfo(Base):
    __tablename__ = "meal_info"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date)
    building = mapped_column(Enum(Building))

    breakfast: Mapped[list["Resaurant"]] = relationship(
        primaryjoin="and_(MealInfo.id==Resaurant.parent_id, " "Resaurant.type=='breakfast')")
    lunch: Mapped[list["Resaurant"]] = relationship(
        primaryjoin="and_(MealInfo.id==Resaurant.parent_id, " "Resaurant.type=='lunch')")
    dinner: Mapped[list["Resaurant"]] = relationship(
        primaryjoin="and_(MealInfo.id==Resaurant.parent_id, " "Resaurant.type=='dinner')")
